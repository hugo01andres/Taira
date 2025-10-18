from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class LeadBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    vacancy_id: int = Field(foreign_key="vacancy.id")
    ai_message: Optional[str] = None
    ai_generated: bool = Field(default=False)
    additional_instructions: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int
    created_at: datetime
    user: Optional["UserRead"] = None
    vacancy: Optional["VacancyRead"] = None


class Lead(LeadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional["User"] = Relationship()
    vacancy: Optional["Vacancy"] = Relationship(back_populates="leads")
