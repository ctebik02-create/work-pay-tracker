import os
import requests

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
