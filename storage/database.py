import sqlite3


DB_NAME = 'app.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    
    CREATE TABLE IF NOT EXISTS 
    shifts ( id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    hours REAL NOT NULL,
    earned REAL NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 
    settings (
    id INTEGER PRIMARY KEY,
    hour_rate REAL NOT NULL,
    default_shift_normal_hours INTEGER NOT NULL,
    salary_period_start_day INTEGER NOT NULL
    )''')

    cursor.execute('''
    SELECT * FROM settings WHERE id = 1''')
    row = cursor.fetchone()
    if row is None:
        cursor.execute('''
        INSERT INTO settings (
        id,
        hour_rate,
        default_shift_normal_hours,
        salary_period_start_day
        )
        VALUES (?, ?, ?, ?)''',
                       (1, 17, 8, 20)
                       )
    conn.commit()
    conn.close()


def get_all_shifts():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursos = conn.cursor()
    cursos.execute('''
    SELECT * FROM shifts''')
    rows = cursos.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_shift_to_db(date, hours, earned):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO shifts (date, hours, earned)
    VALUES (?, ?, ?)''', (date, hours, earned))
    conn.commit()

    shift_id = cursor.lastrowid

    cursor.execute('''SELECT * FROM shifts WHERE id = ?''', (shift_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def delete_shift_from_db(shift_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM shifts WHERE id = ?
    ''', (shift_id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    conn.close()
    if deleted_rows == 0:
        return False
    return True


def update_shift_in_db(shift_id, date, hours, earned):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE shifts SET date = ?, hours = ?, earned = ? 
    WHERE id = ?
    ''', (date, hours, earned, shift_id))
    updated_rows = cursor.rowcount
    conn.commit()
    if updated_rows == 0:
        conn.close()
        return None

    cursor.execute('''
    SELECT * FROM shifts WHERE id = ?
    ''', (shift_id,))

    row = cursor.fetchone()
    conn.close()
    return dict(row)

def get_settings_from_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM settings WHERE id = 1''')
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def update_settings_in_db(hour_rate, default_shift_normal_hours, salary_period_start_day):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE settings 
    SET 
    hour_rate = ?,
    default_shift_normal_hours = ?,
    salary_period_start_day = ?
    WHERE id = 1''', (hour_rate,
                      default_shift_normal_hours,
                      salary_period_start_day))
    conn.commit()

    cursor.execute('''
    SELECT * FROM settings WHERE id = 1''')
    row = cursor.fetchone()
    conn.close()
    return dict(row)