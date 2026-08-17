from fastapi import Depends, HTTPException, status
from .security import get_current_user
from . import models


def require_admin(
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user