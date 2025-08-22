

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse
from app.models import users
from app.utils.auth import verify_password, create_access_token, get_current_user
from app.utils.hashing import hash_password

router = APIRouter(tags=["Users"])

# # ✅ Register
# @router.post("/register", response_model=UserResponse)
# def register(user: UserCreate):
#     existing = users.get_user_by_email(user.email)
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = users.add_user(user.name, user.email, user.password)
#     return new_user  # <-- Already dict from RealDictCursor


@router.post("/register")
def register(user: UserCreate):
    # Check if user already exists
    existing = users.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = users.add_user(user.name, user.email, hashed_pw, user.role)
    
    # Create access token for the new user
    token = create_access_token({"sub": new_user["email"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"],
            "created_at": new_user["created_at"]
        }
    }




@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):  # <-- FIXED
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }





# ✅ Protected profile
@router.get("/me", response_model=UserResponse)
def get_profile(current_user: str = Depends(get_current_user)):
    user = users.get_user_by_email(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # <-- Dict, works with response_model
