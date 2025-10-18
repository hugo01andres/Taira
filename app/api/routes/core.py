from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.company import Company, CompanyCreate, CompanyRead
from app.models.vacancy import Vacancy, VacancyCreate, VacancyRead
from app.models.lead import Lead, LeadCreate, LeadRead
from app.models.user import User
from app.core.auth import get_current_user_from_session, require_auth
from app.services.ai import generate_lead_message

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()




# Companies routes
@router.get("/companies", response_class=HTMLResponse)
async def list_companies(request: Request, session: Session = Depends(get_session)):
    """List all companies."""
    require_auth(request)
    
    companies = session.exec(select(Company)).all()
    return templates.TemplateResponse(
        "companies.html", 
        {"request": request, "companies": companies}
    )


@router.post("/companies", response_class=HTMLResponse)
async def create_company(
    request: Request,
    name: str = Form(...),
    website: str = Form(""),
    session: Session = Depends(get_session)
):
    """Create a new company."""
    require_auth(request)
    
    company = Company(name=name, website=website if website else None)
    session.add(company)
    session.commit()
    session.refresh(company)
    
    return RedirectResponse(url="/companies", status_code=status.HTTP_302_FOUND)


@router.get("/companies/{company_id}/edit", response_class=HTMLResponse)
async def edit_company_page(company_id: int, request: Request, session: Session = Depends(get_session)):
    """Edit company page."""
    require_auth(request)
    
    company = session.exec(select(Company).where(Company.id == company_id)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return templates.TemplateResponse(
        "edit_company.html", 
        {"request": request, "company": company}
    )


@router.post("/companies/{company_id}/edit", response_class=HTMLResponse)
async def update_company(
    company_id: int,
    request: Request,
    name: str = Form(...),
    website: str = Form(""),
    session: Session = Depends(get_session)
):
    """Update a company."""
    require_auth(request)
    
    company = session.exec(select(Company).where(Company.id == company_id)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.name = name
    company.website = website if website else None
    session.add(company)
    session.commit()
    
    return RedirectResponse(url="/companies", status_code=status.HTTP_302_FOUND)


@router.post("/companies/{company_id}/delete", response_class=HTMLResponse)
async def delete_company(
    company_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """Delete a company."""
    require_auth(request)
    
    company = session.exec(select(Company).where(Company.id == company_id)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    session.delete(company)
    session.commit()
    
    return RedirectResponse(url="/companies", status_code=status.HTTP_302_FOUND)


# Vacancies routes
@router.get("/vacancies", response_class=HTMLResponse)
async def list_vacancies(request: Request, session: Session = Depends(get_session)):
    """List all vacancies."""
    require_auth(request)
    
    # Get all vacancies with their companies
    vacancies = session.exec(select(Vacancy)).all()
    for vacancy in vacancies:
        company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
        vacancy.company = company
    
    # Get all companies for the dropdown
    companies = session.exec(select(Company)).all()
    
    return templates.TemplateResponse(
        "vacancies.html", 
        {"request": request, "vacancies": vacancies, "companies": companies}
    )


@router.post("/vacancies", response_class=HTMLResponse)
async def create_vacancy(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    company_id: int = Form(...),
    session: Session = Depends(get_session)
):
    """Create a new vacancy."""
    require_auth(request)
    
    vacancy = Vacancy(
        title=title, 
        description=description if description else None,
        company_id=company_id
    )
    session.add(vacancy)
    session.commit()
    session.refresh(vacancy)
    
    return RedirectResponse(url="/vacancies", status_code=status.HTTP_302_FOUND)


@router.get("/vacancies/{vacancy_id}/edit", response_class=HTMLResponse)
async def edit_vacancy_page(vacancy_id: int, request: Request, session: Session = Depends(get_session)):
    """Edit vacancy page."""
    require_auth(request)
    
    vacancy = session.exec(select(Vacancy).where(Vacancy.id == vacancy_id)).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    # Get company for the vacancy
    company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
    vacancy.company = company
    
    # Get all companies for dropdown
    companies = session.exec(select(Company)).all()
    
    return templates.TemplateResponse(
        "edit_vacancy.html", 
        {"request": request, "vacancy": vacancy, "companies": companies}
    )


@router.post("/vacancies/{vacancy_id}/edit", response_class=HTMLResponse)
async def update_vacancy(
    vacancy_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    company_id: int = Form(...),
    session: Session = Depends(get_session)
):
    """Update a vacancy."""
    require_auth(request)
    
    vacancy = session.exec(select(Vacancy).where(Vacancy.id == vacancy_id)).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    vacancy.title = title
    vacancy.description = description if description else None
    vacancy.company_id = company_id
    session.add(vacancy)
    session.commit()
    
    return RedirectResponse(url="/vacancies", status_code=status.HTTP_302_FOUND)


@router.post("/vacancies/{vacancy_id}/delete", response_class=HTMLResponse)
async def delete_vacancy(
    vacancy_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """Delete a vacancy."""
    require_auth(request)
    
    vacancy = session.exec(select(Vacancy).where(Vacancy.id == vacancy_id)).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    session.delete(vacancy)
    session.commit()
    
    return RedirectResponse(url="/vacancies", status_code=status.HTTP_302_FOUND)


# Leads routes
@router.get("/leads", response_class=HTMLResponse)
async def list_leads(request: Request, session: Session = Depends(get_session)):
    """List all leads for the current user."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's leads
    leads = session.exec(select(Lead).where(Lead.user_id == user.id)).all()
    
    # Get related data for each lead
    for lead in leads:
        vacancy = session.exec(select(Vacancy).where(Vacancy.id == lead.vacancy_id)).first()
        if vacancy:
            company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
            vacancy.company = company
        lead.vacancy = vacancy
    
    # Get all vacancies for the dropdown
    vacancies = session.exec(select(Vacancy)).all()
    for vacancy in vacancies:
        company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
        vacancy.company = company
    
    return templates.TemplateResponse(
        "leads.html", 
        {"request": request, "leads": leads, "user_email": user_email, "vacancies": vacancies}
    )


@router.post("/leads", response_class=HTMLResponse)
async def create_lead(
    request: Request,
    vacancy_id: int = Form(...),
    ai_message: str = Form(""),
    additional_instructions: str = Form(""),
    session: Session = Depends(get_session)
):
    """Create a new lead."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    lead = Lead(
        user_id=user.id,
        vacancy_id=vacancy_id,
        ai_message=ai_message if ai_message else "AI message placeholder",
        additional_instructions=additional_instructions if additional_instructions else None
    )
    session.add(lead)
    session.commit()
    session.refresh(lead)
    
    return RedirectResponse(url="/leads", status_code=status.HTTP_302_FOUND)


@router.post("/leads/{lead_id}/generate", response_class=HTMLResponse)
async def generate_ai_message_for_lead(
    lead_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """Generate AI message for a specific lead."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get the lead
    lead = session.exec(select(Lead).where(Lead.id == lead_id, Lead.user_id == user.id)).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get vacancy and company information
    vacancy = session.exec(select(Vacancy).where(Vacancy.id == lead.vacancy_id)).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        # Generate AI message with user's company context and additional instructions
        ai_message = generate_lead_message(
            vacancy.title, 
            company.name,
            user.company_name,
            user.company_website,
            lead.additional_instructions
        )
        
        # Update the lead with AI message
        lead.ai_message = ai_message
        lead.ai_generated = True
        session.add(lead)
        session.commit()
        
        # Redirect back to leads with success message
        return RedirectResponse(url="/leads?ai_success=true", status_code=status.HTTP_302_FOUND)
        
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"AI generation failed for lead {lead_id}: {e}")
        
        # Redirect back to leads with error message
        return RedirectResponse(url="/leads?ai_error=true", status_code=status.HTTP_302_FOUND)


@router.get("/leads/{lead_id}/edit", response_class=HTMLResponse)
async def edit_lead_page(lead_id: int, request: Request, session: Session = Depends(get_session)):
    """Edit lead page."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get the lead
    lead = session.exec(select(Lead).where(Lead.id == lead_id, Lead.user_id == user.id)).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get vacancy and company information
    vacancy = session.exec(select(Vacancy).where(Vacancy.id == lead.vacancy_id)).first()
    if vacancy:
        company = session.exec(select(Company).where(Company.id == vacancy.company_id)).first()
        vacancy.company = company
    
    # Get all vacancies for dropdown
    vacancies = session.exec(select(Vacancy)).all()
    for v in vacancies:
        company = session.exec(select(Company).where(Company.id == v.company_id)).first()
        v.company = company
    
    return templates.TemplateResponse(
        "edit_lead.html", 
        {"request": request, "lead": lead, "vacancy": vacancy, "vacancies": vacancies}
    )


@router.post("/leads/{lead_id}/edit", response_class=HTMLResponse)
async def update_lead(
    lead_id: int,
    request: Request,
    vacancy_id: int = Form(...),
    ai_message: str = Form(""),
    additional_instructions: str = Form(""),
    session: Session = Depends(get_session)
):
    """Update a lead."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get the lead
    lead = session.exec(select(Lead).where(Lead.id == lead_id, Lead.user_id == user.id)).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.vacancy_id = vacancy_id
    lead.ai_message = ai_message if ai_message else None
    lead.additional_instructions = additional_instructions if additional_instructions else None
    session.add(lead)
    session.commit()
    
    return RedirectResponse(url="/leads", status_code=status.HTTP_302_FOUND)


@router.post("/leads/{lead_id}/delete", response_class=HTMLResponse)
async def delete_lead(
    lead_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """Delete a lead."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get the lead
    lead = session.exec(select(Lead).where(Lead.id == lead_id, Lead.user_id == user.id)).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
        session.delete(lead)
        session.commit()
        
        return RedirectResponse(url="/leads", status_code=status.HTTP_302_FOUND)


# User Profile routes
@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, session: Session = Depends(get_session)):
    """User profile/settings page."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return templates.TemplateResponse(
        "profile.html", 
        {"request": request, "user": user, "user_email": user_email}
    )


@router.post("/profile", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    company_name: str = Form(""),
    company_website: str = Form(""),
    session: Session = Depends(get_session)
):
    """Update user profile."""
    user_email = require_auth(request)
    
    # Get current user
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user profile
    user.company_name = company_name if company_name else None
    user.company_website = company_website if company_website else None
    
    session.add(user)
    session.commit()
    
    return RedirectResponse(url="/profile?updated=true", status_code=status.HTTP_302_FOUND)
