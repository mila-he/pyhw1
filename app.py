from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from data.createDB import Sookla, engine
from datetime import datetime

app = Flask(__name__)

# Loome sessiooniga ühenduse andmebaasiga
Session = sessionmaker(bind=engine)


# API, mis kuvab kõik kohvikud, lisab ja kustutab
@app.route('/kohvikud', methods=['GET', 'POST'])
def kohvikud():
    session = Session()

    if request.method == 'POST':
        method = request.form.get("_method")  # Kontrollime, kas vormis on peidetud meetod

        if method == "DELETE":  # KOHVIKU KUSTUTAMINE
            cafe_id = request.form.get("delete_id")
            kohvik = session.query(Sookla).filter_by(id=cafe_id).first()
            if kohvik:
                session.delete(kohvik)
                session.commit()
            return redirect(url_for('kohvikud'))

        elif method == "PUT":  # KOHVIKU MUUTMINE
            cafe_id = request.form.get("edit_id")
            kohvik = session.query(Sookla).filter_by(id=cafe_id).first()

            if kohvik:
                kohvik.name = request.form.get("name").strip()
                kohvik.location = request.form.get("location").strip()

                if request.form.get("time_open"):
                    kohvik.time_open = datetime.strptime(request.form.get("time_open"), "%H:%M").time()
                if request.form.get("time_closed"):
                    kohvik.time_closed = datetime.strptime(request.form.get("time_closed"), "%H:%M").time()

                session.commit()

            return redirect(url_for('kohvikud'))

        else:  # KOHVIKU LISAMINE
            name = request.form.get("name").strip()
            location = request.form.get("location").strip()
            time_open = request.form.get("time_open")
            time_closed = request.form.get("time_closed")

            if name and location and time_open and time_closed:
                uus_kohvik = Sookla(
                    name=name,
                    location=location,
                    time_open=datetime.strptime(time_open, "%H:%M").time(),
                    time_closed=datetime.strptime(time_closed, "%H:%M").time()
                )
                session.add(uus_kohvik)
                session.commit()
                return redirect(url_for('kohvikud'))

    # AVAMISAJA FILTREERIMINE
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if start_time and end_time:
        try:
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()

            kohvikud = session.query(Sookla).filter(
                Sookla.time_open <= start_time,
                Sookla.time_closed >= end_time
            ).all()
        except ValueError:
            kohvikud = []
    else:
        kohvikud = session.query(Sookla).all()

    session.close()
    return render_template("kohvikud.html", kohvikud=kohvikud)


if __name__ == '__main__':
    app.run(debug=True)
