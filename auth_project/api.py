from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models_sqlalchemy import models, database
from pydantic import BaseModel

app = FastAPI()

# Dependency to get the database session
get_db = database.get_db

# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str
    password: str

# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user. Checks if the user already exists and returns an error if so.
    """
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(username=user.username, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username}

@app.post("/auth/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Handle user login. Checks if the username and password match.
    """
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    # This example does not hash passwords correctly, only compares as plain text.
    # Ensure that hashed passwords are used in a real-world scenario.
    if db_user.hashed_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"message": "Login successful", "username": db_user.username}

# Add a root path endpoint
@app.get("/")
def read_root():
    """
    Simple root endpoint for health checking.
    """
    return {"message": "Welcome to the FastAPI root endpoint!"}
