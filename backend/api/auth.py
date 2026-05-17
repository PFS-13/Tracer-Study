from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verify_token

from services.auth_services import (
    register_user,
    login_user
)

from schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

router = APIRouter( prefix="/auth",tags=["Authentication"])


@router.post("/register")
def register(data: RegisterRequest,db: Session = Depends(get_db)):
    user = register_user(db,data.email,data.password)

    if not user:
        raise HTTPException(status_code=400,detail="Email sudah terdaftar"
        )
    return {
        "message": "Register success"
    }


@router.post("/login",response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    token = login_user(
        db,
        data.email,
        data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: str = Depends(verify_token)
):

    return {
        "message": "Protected route success",
        "email": current_user
    }