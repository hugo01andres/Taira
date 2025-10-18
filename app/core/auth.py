from fastapi import Request, HTTPException, status


def get_current_user_from_session(request: Request):
    """Get current user from session."""
    return request.session.get("user")


def require_auth(request: Request):
    """Check if user is authenticated."""
    user_email = get_current_user_from_session(request)
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_email
