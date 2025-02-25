import os
from sqlalchemy import create_engine, Column, Integer, String, inspect, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use the script's directory as the base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'kohvikud.db')


# Create the engine and declarative base using an absolute path
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Base = declarative_base()


class Sookla(Base):
    __tablename__ = 'sookla'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    time_open = Column(Time, nullable=False)
    time_closed = Column(Time, nullable=False)


Session = sessionmaker(bind=engine)


def create_database_and_tables():
    inspector = inspect(engine)
    if not inspector.has_table('sookla'):
        Base.metadata.create_all(engine)
        print("Andmebaasi loomine edukas!")
    else:
        print("Andmebaas on juba olemas!")


if __name__ == '__main__':
    create_database_and_tables()
