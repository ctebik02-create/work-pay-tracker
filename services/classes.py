
from datetime import date
from services.periods import  get_current_period_start, get_current_period_end

class SummaryService:
    def __init__(self, shifts: list, period_start_day: int):
        self.shifts = shifts
        self.period_start_day = period_start_day

    def __str__(self):
        return f"shifts: {self.shifts}, period: {self.period_start_day} "
    def __repr__(self):
        return f"SummaryService(shifts: {self.shifts}, period: {self.period_start_day} )"

    @property
    def period_start(self):
        return get_current_period_start(self.period_start_day)

    @property
    def period_end(self):
        return get_current_period_end(self.period_start, self.period_start_day)

    @staticmethod
    def calculate_earned(hours: float, rate: float) -> float:
        return hours * rate

    def _get_filtered_shifts(self) -> list[dict]:
        filtered_shifts = []

        for shift in self.shifts:
            shift_date = date.fromisoformat(shift['date'])
            if self.period_start <= shift_date <= self.period_end:
                filtered_shifts.append(shift)
        return filtered_shifts

    def get_summary(self) -> dict:
        filtered_shifts = self._get_filtered_shifts()
        total_earned = sum(shift['earned'] for shift in filtered_shifts)
        total_hours = sum(shift['hours'] for shift in filtered_shifts)
        total_shifts = len(filtered_shifts)
        if total_earned > 0:
            average_earned = total_earned / total_shifts
            average_hours = total_hours / total_shifts
        else:
            average_earned = 0
            average_hours = 0

        summary = {
            'total_earned': total_earned,
            'total_hours': total_hours,
            'total_shifts': total_shifts,
            'average_earned': average_earned,
            'average_hours': average_hours,
            'period_start': str(self.period_start),
            'period_end': str(self.period_end),
        }
        return summary

class ReflectionService(SummaryService):
    def __init__(self, shifts: list, period_start_day: int, currency: str = 'EUR'):
        super().__init__(shifts, period_start_day)
        self.currency = currency

    def get_reflection_data(self) -> dict:
        data = self.get_summary()
        notes = []
        for shift in self._get_filtered_shifts():
            note = shift['note']
            if note is not None and note.strip() != '':
                notes.append({'date': shift['date'], 'note': note})
        data.update({
            'notes': notes,
            'currency': self.currency,
        })
        return data