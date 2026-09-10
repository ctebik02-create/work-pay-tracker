from storage.orm import engine, User, Shift, Settings
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session


with engine.connect() as conn:
    print('Database connection is successful')

#Shifts
def add_shift_to_database(date, hours, earned, note, user_id):
    shift = Shift(
        date=date,
        hours=hours,
        earned=earned,
        note=note,
        user_id=user_id,
        
    )
    with Session(engine) as session:
        session.add(shift)
        session.commit()
        session.refresh(shift)
        return shift

def get_all_shifts_from_database(user_id):
    statement = select(Shift).where(Shift.user_id == user_id).order_by(Shift.id)
    with Session(engine) as session:
        return session.scalars(statement).all()

def delete_shift_from_database(shift_id, user_id):
    statement = delete(Shift).where(Shift.id == shift_id, Shift.user_id == user_id)
    with Session(engine) as session:
        result = session.execute(statement)
        session.commit()
        return result.rowcount > 0

def update_shift_in_database(user_id, shift_id, date, hours, earned, note):
    statement = select(Shift).where(Shift.user_id == user_id, Shift.id == shift_id)
    with Session(engine) as session:
        shift = session.scalar(statement)
        if shift is None:
            return None
        shift.date = date
        shift.hours = hours
        shift.earned = earned
        shift.note = note
        session.commit()
        session.refresh(shift)
        return shift

#Settings
def get_settings_from_database():
    with Session(engine) as session:
        settings = session.get(Settings, 1)
        return settings

def update_settings_in_database(hour_rate, default_shift_normal_hours, salary_period_start_day):
    with Session(engine) as session:
        settings = session.get(Settings, 1)
        if settings is None:
            return None
        settings.hour_rate = hour_rate
        settings.default_shift_normal_hours = default_shift_normal_hours
        settings.salary_period_start_day = salary_period_start_day
        session.commit()
        session.refresh(settings)
        return settings


#Users
def get_user_by_username(username):
    statement = select(User).where(User.username == username)

    with Session(engine) as session:
        user = session.scalar(statement)
        return user

def create_user(username, password):
    with Session(engine) as session:
        user = User(username=username, password_hash=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def delete_user(user_id):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            return None
        session.delete(user)
        session.commit()
        return True