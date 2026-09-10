from fastapi import APIRouter, HTTPException, Depends
from models.schemas import ShiftCreate, ShiftResponse
from services.aisummary import generate_ai_summary, generate_ai_reflection
from services.classes import ReflectionService, SummaryService
from routes.auth import get_current_user

from storage.orm_base import add_shift_to_database, get_all_shifts_from_database, delete_shift_from_database
from storage.orm_base import update_shift_in_database, get_settings_from_database
from storage.orm import Settings


router = APIRouter()

def get_settings():
    return get_settings_from_database()


def get_shifts(user_id: int = Depends(get_current_user)):
    return get_all_shifts_from_database(user_id)


@router.get('/shifts', response_model=list[ShiftResponse])
def list_shifts(shifts: list = Depends(get_shifts)):
    return shifts


@router.post('/shifts', response_model=ShiftResponse)
def post_shifts(shifts: ShiftCreate, settings: Settings = Depends(get_settings), user_id: int = Depends(get_current_user)):
    rate = settings.hour_rate
    earned = SummaryService.calculate_earned(shifts.hours, rate)
    new_shifts = add_shift_to_database(shifts.date, shifts.hours, earned, shifts.note, user_id)
    return new_shifts

@router.get('/summary')
def get_summary(shifts: list = Depends(get_shifts),
                                  settings: Settings = Depends(get_settings)):
    services = SummaryService(shifts=shifts, period_start_day=settings.salary_period_start_day)
    return services.get_summary()

@router.get('/summary/ai')
def get_ai_summary(shifts: list = Depends(get_shifts),
                                  settings: Settings = Depends(get_settings)):
    services = SummaryService(shifts=shifts, period_start_day=settings.salary_period_start_day)

    summary = services.get_summary()
    try:
        text = generate_ai_summary(summary)
    except Exception:
        text = "AI summary unavailable"
    return {
        "summary_text": text,
    }

@router.delete('/shifts/{shift_id}')
def delete_shift(shift_id : int, user_id: int = Depends(get_current_user)):
    result = delete_shift_from_database(shift_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Shift not found")

    return {"status": "ok"}

@router.put('/shifts/{shift_id}', response_model=ShiftResponse)
def update_shift(shift_id : int, shift : ShiftCreate, settings: Settings = Depends(get_settings),
                 user_id: int = Depends(get_current_user)):
    hour_rate = settings.hour_rate
    earned = SummaryService.calculate_earned(shift.hours, hour_rate)

    result = update_shift_in_database(
        user_id,
        shift_id,
        shift.date,
        shift.hours,
        earned,
        shift.note,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Shift not found")
    return result

@router.get('/reflection/current-period')
def get_current_period_reflection(shifts: list = Depends(get_shifts),
                                  settings: Settings = Depends(get_settings)):


    service = ReflectionService(shifts=shifts, period_start_day=settings.salary_period_start_day)
    data = service.get_reflection_data()
    text = generate_ai_reflection(data)
    return {
        "reflection_text": text,
    }