from datetime import datetime

from fastapi import Depends,FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Organization

class OrganizationCreate(BaseModel):
    name: str

class OrganizationResponse(BaseModel):
    id : int
    name : str
    created_at : datetime
    updated_at : datetime

    model_config ={
        "from_attributes" : True
    }

app = FastAPI(
    title = "Saas Platform API",
    description = "APIs for Saas Platform",
    version = "1.0.0"
)


@app.get("/health" , tags =["Health"])
def health_check():
    return {
        "status" : "healthy",
        "app_title" : "Saas Platform",
        "version" : "1.0.0"
    }

@app.post("/organizations",response_model=OrganizationResponse)
def create_organization(organization : OrganizationCreate,db:Session = Depends(get_db)):
    new_organization = Organization(
        name = organization.name
    )
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization

@app.get("/organizations",response_model=list[OrganizationResponse])
def get_organizations(db : Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return organizations