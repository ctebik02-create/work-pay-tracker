from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class SettingsUpdate(BaseModel):
    hour_rate: float = Field(gt=0)
    default_shift_normal_hours: int = Field(gt=0)
    salary_period_start_day: int = Field(ge=0, le=28)

class ShiftCreate(BaseModel):
    date: date
    hours: float = Field(gt=0, le=24)
    note: str | None = None

class ShiftResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    date: date
    hours: float
    earned: float
    note: str | None = None
    user_id: int

class SettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    hour_rate: float
    default_shift_normal_hours: int
    salary_period_start_day: int
    user_id: int | None = None

