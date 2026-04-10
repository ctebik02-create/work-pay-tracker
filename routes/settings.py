from fastapi import APIRouter
from models.schemas import SettingsUpdate
from storage.database import get_settings_from_db, update_settings_in_db

router = APIRouter()

@router.get('/settings')
def get_settings():
    return get_settings_from_db()

@router.put('/settings')
def update_settings(settings: SettingsUpdate):
    return update_settings_in_db(settings.hour_rate,
                                  settings.default_shift_normal_hours,
                                  settings.salary_period_start_day)
