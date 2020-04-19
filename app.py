# 1. import Flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def trip():
    print("All available routes")
    r return(
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"   
        )  

@app.route("/api/v1.0/precipitation")
def precipitation():
#  * Query for the dates and precipitation observations from the last year.
#  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#  * Return the json representation of your dictionary.
   last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
   last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    rain_totals = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

#########################################################################################
@app.route("/api/v1.0/stations")
def stations():
# * Return a JSON list of stations from the dataset.
      stations = session.query(Station.station,Station.name).all()
    return jsonify(stations)

#########################################################################################

@app.route("/api/v1.0/tobs")
def tobs():

#   * Query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year. 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date,Measurement.tobs).\
                            filter(Measurement.date > last_year).\
                            order_by(Measurement.date).all()
    return jsonify(tobs)  

#########################################################################################

@app.route("/api/v1.0/<start>")
def startDate(date):
# * When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_Date= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(start_Date)

@app.route("/api/v1.0/<start>/<end>")
# * When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
def startDateEndDate(start,end):
    Dates_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(Dates_results)