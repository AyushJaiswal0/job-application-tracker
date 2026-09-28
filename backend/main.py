from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

from database import engine, Base, SessionLocal, get_db
from security import hash_password, verify_password
from auth import create_access_token, get_current_user_id
import models

class Application(BaseModel):
    company: str
    job_title: str
    location: str
    status: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


app = FastAPI(
    title="Job Application Tracker API",
    description="REST API for managing job application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Job Application Tracker API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy" 
    }

@app.get("/applications")
def get_applications(
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db= Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
    ):

    query = db.query(models.Application).filter(
        models.Application.user_id == user_id
    )

    if status:
        query = query.filter(models.Application.status == status)

    if search:
        query = query.filter(
            (models.Application.company.contains(search.lower())) |
            (models.Application.job_title.contains(search.lower()))
        )

    return query.all()


@app.get("/applications/{application_id}")
def get_application(application_id: int, db=Depends(get_db), user_id: int = Depends(get_current_user_id)):
    application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id
    ).first()

    if application is None:
       raise HTTPException(
           status_code=404,
           detail="Application not found"
       )
    
    return application

@app.post("/applications")
def create_applications(application: Application, db=Depends(get_db), user_id: int = Depends(get_current_user_id)):
    new_application = models.Application(
        company = application.company,
        job_title = application.job_title,
        location = application.location,
        status = application.status,
        user_id = user_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application created successfully",
        "application": new_application
    }


@app.put("/applications/{application_id}")
def update_application(application_id: int, application:Application, db=Depends(get_db), user_id: int = Depends(get_current_user_id)):
    existing_application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id
    ).first()

    if existing_application is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    existing_application.company = application.company
    existing_application.job_title = application.job_title
    existing_application.location = application.location
    existing_application.status = application.status

    db.commit()
    db.refresh(existing_application)

    return existing_application


@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db=Depends(get_db), user_id: int = Depends(get_current_user_id)):
    application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id
    ).first()

    if application is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }


@app.post("/register")
def register_user(user:UserCreate, db=Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "username": new_user.username
    }

@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = verify_password(form_data.password, existing_user.password)

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(existing_user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(user_id: int=Depends(get_current_user_id)):
    return {
        "user_id": user_id
    }


@app.get("/dashboard/stats")
def get_dashboard_stats(
    db = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    applications = db.query(models.Application).filter(
        models.Application.user_id == user_id
    ).all()

    total = len(applications)

    applied = sum(
        1 for application in applications if application.status.lower() == "applied"
    )

    interview = sum(
        1 for application in applications if application.status.lower() == "interview"
    )

    rejected = sum(
        1 for application in applications if application.status.lower() == "rejected"
    )

    offer = sum(
        1 for application in applications if application.status.lower() == "offer"
    )

    return {
        "total": total,
        "applied": applied,
        "interview": interview,
        "rejected": rejected,
        "offer": offer
    }