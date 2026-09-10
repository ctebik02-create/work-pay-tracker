from fastapi import APIRouter
from models.schemas import SettingsUpdate


from storage.orm_base import update_settings_in_database, get_settings_from_database

router = APIRouter()

@router.get('/settings', response_model=SettingsUpdate)
def get_settings():
    return get_settings_from_database()

@router.put('/settings', response_model=SettingsUpdate)
def update_settings(settings: SettingsUpdate):
    return update_settings_in_database(settings.hour_rate,
                                  settings.default_shift_normal_hours,
                                  settings.salary_period_start_day)
