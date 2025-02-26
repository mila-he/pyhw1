from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from database.createDB import Session, Sookla

app = Flask(__name__)


@app.route('/kohvikud', methods=["GET", "POST"])
def kohvikud():
    session = Session()

    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        time_open = request.form.get("time_open")
        time_closed = request.form.get("time_closed")

        time_open = datetime.strptime(time_open, "%H:%M").time()
        time_closed = datetime.strptime(time_closed, "%H:%M").time()

        new_kohvik = Sookla(Name=name, Location=location, time_open=time_open, time_closed=time_closed)
        session.add(new_kohvik)
        session.commit()
        session.close()

        return redirect(url_for("kohvikud"))

    else:
        start_time = request.args.get("start")
        end_time = request.args.get("end")

        if start_time and end_time:
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()

            kohvikud = session.query(Sookla).filter(
                Sookla.time_open <= start_time,
                Sookla.time_closed >= end_time
            ).all()
        else:
            kohvikud = session.query(Sookla).all()

        session.close()
        return render_template("index.html", kohvikud=kohvikud)


if __name__ == '__main__':
    app.run(debug=True)
