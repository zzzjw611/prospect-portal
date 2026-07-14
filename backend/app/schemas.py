from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class LeadStatus(StrEnum):
    pending = "PENDING"
    reached_out = "REACHED_OUT"


class Lead(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    resume_filename: str
    status: LeadStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LeadCreated(BaseModel):
    id: str
    status: LeadStatus
    message: str


class LeadStatusUpdate(BaseModel):
    status: LeadStatus

