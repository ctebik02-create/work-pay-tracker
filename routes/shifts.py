from fastapi import APIRouter, HTTPException
from models.schemas import ShiftCreate
from services.periods import get_current_period_start, get_current_period_end
from datetime import date
from storage.database import add_shift_to_db, get_all_shifts, delete_shift_from_db, update_shift_in_db
from storage.database import get_settings_from_db

router = APIRouter()



@router.get('/shifts')
def get_shifts():
    return get_all_shifts()


@router.post('/shifts')
def post_shifts(shifts: ShiftCreate):
    settings = get_settings_from_db()
    hour_rate = settings["hour_rate"]
    earned = hour_rate * shifts.hours
    new_shifts = add_shift_to_db(shifts.date, shifts.hours, earned)
    return new_shifts

@router.get('/summary')
def get_summary():
    settings = get_settings_from_db()
    period_start_day = settings["salary_period_start_day"]
    period_start = get_current_period_start(period_start_day)
    period_end = get_current_period_end(period_start, period_start_day)
    filtered_shifts = []
    shifts = get_all_shifts()
    for shift in shifts:
        shift_date = date.fromisoformat(shift['date'])
        if period_start <= shift_date <= period_end:
            filtered_shifts.append(shift)


    total_earned = sum(shift['earned'] for shift in filtered_shifts)
    total_hours = sum(shift['hours'] for shift in filtered_shifts)
    total_shifts = len(filtered_shifts)
    summary = {
        "total_earned": total_earned,
        'total_hours': total_hours,
        'total_shifts': total_shifts,
        'period_start': period_start,
        'period_end': period_end,
    }
    return summary

@router.delete('/shifts/{shift_id}')
def delete_shift(shift_id : int):
    result = delete_shift_from_db(shift_id)
    if not result:
        raise HTTPException(status_code=404, detail="Shift not found")

    return {"status": "ok"}

@router.put('/shifts/{shift_id}')
def update_shift(shift_id : int, shift : ShiftCreate):
    settings = get_settings_from_db()
    hour_rate = settings['hour_rate']
    earned = hour_rate * shift.hours

    result = update_shift_in_db(
        shift_id,
        shift.date,
        shift.hours,
        earned
    )
    if not result:
        raise HTTPException(status_code=404, detail="Shift not found")
    return result
