import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

from database.db_session import get_connection

load_dotenv()  # Load environment variables from .env file
# security config

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set. Please set it in your .env file.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# this tells FastAPI where the frontend should send credentials to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic schemas
class UserCreate(BaseModel):
    email: EmailStr # to validate email format
    password: str

class UserLogin(BaseModel):
    email: str # validation not needed anymore
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# utility

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# endpoints

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # check if email exists already
            cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # hash pswd and insert new user
            hashed_pwd = get_password_hash(user.password)
            cur.execute(
                "INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id", 
                (user.email, hashed_pwd)
            )
            new_user_id = cur.fetchone()[0]
            conn.commit()

            # mint JWT token
            access_token = create_access_token(data={"sub": str(new_user_id)})
            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        logging.error(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # look up user
            cur.execute("SELECT id, hashed_password FROM users WHERE email = %s", (form_data.username,))
            db_user = cur.fetchone()
            
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id, hashed_pwd = db_user
            
            # verify password mathematically
            if not verify_password(form_data.password, hashed_pwd):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # mint JWT Token
            access_token = create_access_token(data={"sub": str(user_id)})
            return {"access_token": access_token, "token_type": "bearer"}
    finally:
        conn.close()

# auth dependency to protect routes
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Plug this into any endpoint to force the user to be logged in.
    It decrypts their JWT and returns their Postgres User ID.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except JWTError:
        raise credentials_exception