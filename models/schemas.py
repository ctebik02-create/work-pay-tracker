from pydantic import BaseModel, Field
from datetime import date

class SettingsUpdate(BaseModel):
    hour_rate: float = Field(gt=0)
    default_shift_normal_hours: int = Field(gt=0)
    salary_period_start_day: int = Field(ge=0, le=28)

class ShiftCreate(BaseModel):
    date: date
    hours: float = Field(gt=0, le=24)
    note: str | None = None


