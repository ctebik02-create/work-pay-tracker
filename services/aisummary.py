import os
import requests
from storage.database import get_all_shifts, get_settings_from_db
from services.periods import get_current_period_start, get_current_period_end
from datetime import date

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

def generate_ai_summary(summary: dict) -> str:
    prompt = f"""
You are writing a short personal work summary for the user.

Write a short, natural, friendly summary of this pay period in 3-4 sentences.
Use simple language.
Do not sound corporate or overly formal.
Do not invent information that is not in the data.
Focus on the workload, total earnings, and overall pattern of the period.

Data:
Period start: {summary['period_start']}
Period end: {summary['period_end']}
Total shifts: {summary['total_shifts']}
Total hours: {summary['total_hours']}
Total earned: {summary['total_earned']}
Average hours per shift: {summary['average_hours']}
Average earned per shift: {summary['average_earned']}

Make it sound human and concise.
"""
    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "upstage/solar-10.7b-instruct",
            "messages": [
                {"role": 'user', 'content': prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.5,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def build_reflection_data():
    shifts = get_all_shifts()
    settings = get_settings_from_db()
    period_start_day = settings["salary_period_start_day"]
    period_start = get_current_period_start(period_start_day)
    period_end = get_current_period_end(period_start, period_start_day)
    filtered_shifts = []
    for shift in shifts:
        shift_date = date.fromisoformat(shift['date'])
        if period_start <= shift_date <= period_end:
            filtered_shifts.append(shift)
    notes = []
    for shift in filtered_shifts:
        note = shift['note']
        if note is not None and note.strip() != "":
            notes.append({'date': shift['date'], 'note': note})

    total_earned = sum(shift['earned'] for shift in filtered_shifts)
    total_hours = sum(shift['hours'] for shift in filtered_shifts)
    total_shifts = len(filtered_shifts)

    if total_shifts > 0:
        average_hours = total_hours / total_shifts
        average_earned = total_earned / total_shifts
    else:
        average_hours = 0
        average_earned = 0

    data = {
        "period_start": str(period_start),
        "period_end": str(period_end),
        "total_shifts": total_shifts,
        "total_hours": total_hours,
        "total_earned": total_earned,
        "average_hours": average_hours,
        "average_earned": average_earned,
        "notes": notes,
    }
    return data

def generate_ai_reflection(data):
    if not data["notes"]:
        return "No notes available for reflection in the current period."
    else:
        formatted_notes = '\n'.join(
            f"{item['date']}: {item['note']}"
            for item in data["notes"]
        )

        prompt = f'''
You are analyzing a user's work period based only on real data.

Your task is to write a short, honest, useful reflection.

Important rules:
- Use only the provided data.
- Do not invent facts.
- Do not exaggerate patterns.
- If there are only one or two notes, clearly say that insights are limited.
- If evidence is weak, use cautious language such as:
  "may suggest", "seems", "limited data shows".
- Currency is EUR (€).
- Keep the tone natural, clear, and helpful.
- Do not sound corporate, robotic, or overly formal.
- Keep the answer concise.
- Do not give health, burnout, or emotional advice unless directly
supported by the notes.
- If there is only one note, state that there is not enough data to identify
repeated themes.
- When data is limited, keep the takeaway practical and modest.

Write exactly 4 bullet points:

1. Overall tone of the period
2. Repeated themes or observations from the notes
3. Workload insight based on stats and notes
4. One short practical takeaway

Work Period Data:

Period start: {data['period_start']}
Period end: {data['period_end']}
Total shifts: {data['total_shifts']}
Total hours: {data['total_hours']}
Total earned: {data['total_earned']}
Average hours per shift: {data['average_hours']}
Average earned per shift: {data['average_earned']}
Notes: 
{formatted_notes}'''
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "upstage/solar-10.7b-instruct",
                "messages": [
                    {"role": 'user', 'content': prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.5,
            },
            timeout=30,
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]