import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shifts (
                    id SERIAL PRIMARY KEY,
                    date TEXT NOT NULL,
                    hours REAL NOT NULL,
                    earned REAL NOT NULL
                )
            """)

            cursor.execute('''
            ALTER TABLE shifts ADD COLUMN IF NOT EXISTS note TEXT''')

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    hour_rate REAL NOT NULL,
                    default_shift_normal_hours INTEGER NOT NULL,
                    salary_period_start_day INTEGER NOT NULL
                )
            """)

            cursor.execute("""
                SELECT * FROM settings WHERE id = %s
            """, (1,))
            row = cursor.fetchone()

            if row is None:
                cursor.execute("""
                    INSERT INTO settings (
                        id,
                        hour_rate,
                        default_shift_normal_hours,
                        salary_period_start_day
                    )
                    VALUES (%s, %s, %s, %s)
                """, (1, 17, 8, 20))


def get_all_shifts():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM shifts
                ORDER BY id
            """)
            rows = cursor.fetchall()
            return rows


def add_shift_to_db(date, hours, earned, note):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO shifts (date, hours, earned, note)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (date, hours, earned, note))
            row = cursor.fetchone()
            return row


def delete_shift_from_db(shift_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM shifts
                WHERE id = %s
            """, (shift_id,))
            return cursor.rowcount > 0


def update_shift_in_db(shift_id, date, hours, earned, note):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE shifts
                SET date = %s, hours = %s, earned = %s, note = %s
                WHERE id = %s
                RETURNING *
            """, (date, hours, earned, note, shift_id))
            row = cursor.fetchone()
            return row


def get_settings_from_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM settings WHERE id = %s
            """, (1,))
            row = cursor.fetchone()
            return row


def update_settings_in_db(hour_rate, default_shift_normal_hours, salary_period_start_day):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE settings
                SET
                    hour_rate = %s,
                    default_shift_normal_hours = %s,
                    salary_period_start_day = %s
                WHERE id = %s
                RETURNING *
            """, (
                hour_rate,
                default_shift_normal_hours,
                salary_period_start_day,
                1
            ))
            row = cursor.fetchone()
            return row