from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class CompanyBase(SQLModel):
    name: str = Field(index=True)
    website: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime


class Company(CompanyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    vacancies: List["Vacancy"] = Relationship(back_populates="company")
