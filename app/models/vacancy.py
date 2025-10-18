from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class VacancyBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    company_id: int = Field(foreign_key="company.id")


class VacancyCreate(VacancyBase):
    pass


class VacancyRead(VacancyBase):
    id: int
    created_at: datetime
    company: Optional["CompanyRead"] = None


class Vacancy(VacancyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    company: Optional["Company"] = Relationship(back_populates="vacancies")
    leads: List["Lead"] = Relationship(back_populates="vacancy")
