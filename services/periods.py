from datetime import date, timedelta

def get_current_period_start(period_start_day: int):
    today = date.today()
    if today.day >= period_start_day:
        return date(today.year, today.month, period_start_day)
    else:
        if today.month == 1:
            month = 12
            year = today.year - 1
            return date(year, month, period_start_day)
        else:
            month = today.month - 1
            return date(today.year, month, period_start_day)

def get_current_period_end(period_start : date, period_start_day: int):
    month = period_start.month
    year = period_start.year
    if month < 12:
        next_month = month + 1
        next_year = year
    else:
        next_month = 1
        next_year = year + 1

    next_period_start = date(next_year, next_month, period_start_day)
    period_end = next_period_start - timedelta(days=1)
    return period_end
