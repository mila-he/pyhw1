import os
from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.orm import declarative_base, sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "kohvikud.db")

engine = create_engine(f"sqlite:///{db_path}")  # Engine is the starting point for any SQLAlchemy application.
Base = declarative_base()  # Create the base class using the declarative_base() function.


class Sookla(Base):  # Loome "base" külge mapped classi (SOOKLA - tabel).
    __tablename__ = 'SOOKLA'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Location = Column(String, nullable=False)
    time_open = Column(Time, nullable=False)
    time_closed = Column(Time, nullable=False)

    def __str__(self):
        return f" Kohvik: {self.Name}, aadressil: {self.Location}, avatud: {self.time_open}-{self.time_closed}"


Session = sessionmaker(bind=engine)  # In order to interact with DB, we need to obtain its handle.


def create_database():
    Base.metadata.create_all(engine)
    print("Andmebaas ja tabel SOOKLA on loodud.")


if __name__ == "__main__":
    create_database()
