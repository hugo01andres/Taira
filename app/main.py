from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select
from .core.config import settings
from .core.database import init_db, get_session
from .core.security import verify_password, get_password_hash
from .api.routes.auth import router as auth_router
from .api.routes.core import router as core_router
from .api.deps import get_current_user
from .models.user import User

app = FastAPI(title=settings.app_name)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(core_router, tags=["core"])


@app.on_event("startup")
async def startup_event():
    # Validate security configuration
    security_errors = settings.validate_security_config()
    if security_errors:
        print("🚨 SECURITY WARNINGS:")
        for error in security_errors:
            print(f"   ⚠️  {error}")
        print("   Please update your .env file with proper security settings")
    
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root route - redirect to dashboard if logged in, otherwise to login."""
    user_email = get_current_user_from_session(request)
    if user_email:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.env}


# Import authentication functions
from .core.auth import get_current_user_from_session


# Frontend routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Process login form."""
    # Find user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid email or password"}
        )
    
    if not user.is_active:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Account is inactive"}
        )
    
    # Store user in session
    request.session["user"] = user.email
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Process registration form."""
    # Check if user already exists
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Store user in session
    request.session["user"] = user.email
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard page - requires authentication."""
    user_email = get_current_user_from_session(request)
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user_email": user_email}
    )


@app.get("/logout")
async def logout_user(request: Request):
    """Logout user and clear session."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """Protected route that requires authentication."""
    return {
        "message": "This is a protected route",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "is_active": current_user.is_active
        }
    }
