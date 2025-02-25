import os
import csv
from datetime import datetime
from createDB import Session, Sookla


def import_data_csv(csv_file):
    # Kontrollime, kas andmebaas eksisteerib
    if not os.path.exists("kohvikud.db"):
        print("Andmebaasi ei leitud! Palun käivita esmalt `createDB.py`.")
        return  # Peatame funktsiooni, et vältida viga

    session = Session()
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check that the row has at least 5 columns
                if len(row) < 5:
                    continue

                name = row[0].strip()
                location = row[1].strip()
                time_open = datetime.strptime(row[3].strip(), "%H:%M").time()
                time_closed = datetime.strptime(row[4].strip(), "%H:%M").time()

                new_record = Sookla(
                    name=name,
                    location=location,
                    time_open=time_open,
                    time_closed=time_closed
                )
                session.add(new_record)

        session.commit()
        print("Andmed  edukalt lisatud!")
    except FileNotFoundError:
        print(f"CSV faili ei õnnestunud leida!")
    finally:
        session.close()


if __name__ == '__main__':
    # Use an absolute path for the CSV file, too:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(BASE_DIR, 'Kohvikud.csv')
    import_data_csv(csv_file_path)
