from datetime import datetime
from createDB import Sookla, Session


def load_data_from_csv(file_path):
    session = Session()  # Loome SQLAlchemy sessiooni

    with open(file_path, "r", encoding="utf-8") as file:
        data = [line.strip().split(",") for line in file]

    for row in data:
        session.add(Sookla(
            Name=row[0],
            Location=row[1],
            time_open=datetime.strptime(row[3].strip(), "%H:%M").time(),
            time_closed=datetime.strptime(row[4].strip(), "%H:%M").time()
        ))

    session.commit()  # Salvestame andmed andmebaasi
    session.close()  # Sulgeme sessiooni
    print("Andmed on edukalt lisatud andmebaasi.")


if __name__ == "__main__":
    file_path = "Kohvikud.csv"
    load_data_from_csv(file_path)
