from urllib.parse import uses_relative

from storage.orm import engine, User
from sqlalchemy import select
from sqlalchemy.orm import Session


with engine.connect() as conn:
    print('Database connection is successful')

with Session(engine) as session:
    users = session.scalars(select(User)).all()
    print(users)