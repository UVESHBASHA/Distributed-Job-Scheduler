from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.config import ALGORITHM, SECRET_KEY
from app.auth.oauth2 import oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify JWT token and return the current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": user_id, "email": email}
