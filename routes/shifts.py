from fastapi import APIRouter, HTTPException, Depends
from models.schemas import ShiftCreate
from storage.database import add_shift_to_db, get_all_shifts, delete_shift_from_db, update_shift_in_db
from storage.database import get_settings_from_db
from services.aisummary import generate_ai_summary, generate_ai_reflection
from services.classes import ReflectionService, SummaryService
from routes.auth import get_current_user

router = APIRouter()

def get_settings():
    return get_settings_from_db()


def get_shifts():
    return get_all_shifts()


@router.get('/shifts')
def list_shifts(shifts: list = Depends(get_shifts), user_id: int = Depends(get_current_user)):
    return shifts


@router.post('/shifts')
def post_shifts(shifts: ShiftCreate, settings: dict = Depends(get_settings), user_id: int = Depends(get_current_user)):
    rate = settings["hour_rate"]
    earned = SummaryService.calculate_earned(shifts.hours, rate)
    new_shifts = add_shift_to_db(shifts.date, shifts.hours, earned, shifts.note)
    return new_shifts

@router.get('/summary')
def get_summary(shifts: list = Depends(get_shifts),
                                  settings: dict = Depends(get_settings), user_id: int = Depends(get_current_user)):
    services = SummaryService(shifts=shifts, period_start_day=settings['salary_period_start_day'])
    return services.get_summary()

@router.get('/summary/ai')
def get_ai_summary(shifts: list = Depends(get_shifts),
                                  settings: dict = Depends(get_settings), user_id: int = Depends(get_current_user)):
    services = SummaryService(shifts=shifts, period_start_day=settings['salary_period_start_day'])

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
    result = delete_shift_from_db(shift_id)
    if not result:
        raise HTTPException(status_code=404, detail="Shift not found")

    return {"status": "ok"}

@router.put('/shifts/{shift_id}')
def update_shift(shift_id : int, shift : ShiftCreate, settings: dict = Depends(get_settings),
                 user_id: int = Depends(get_current_user)):
    hour_rate = settings['hour_rate']
    earned = SummaryService.calculate_earned(shift.hours, hour_rate)

    result = update_shift_in_db(
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
                                  settings: dict = Depends(get_settings), user_id: int = Depends(get_current_user)):


    service = ReflectionService(shifts=shifts, period_start_day=settings["salary_period_start_day"])
    data = service.get_reflection_data()
    text = generate_ai_reflection(data)
    return {
        "reflection_text": text,
    }