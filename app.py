import sqlite3
import datetime
import time

from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/houses')
def houses():
    conn = sqlite3.connect('sanfrancisco.db')

    c=conn.cursor()
    c.execute("SELECT Address, Longitude, Latitude, Sold_Price, Bedroom, Bathroom, Sq_ft, Days_on_Market FROM Address")

    rows=c.fetchall()
    output = []

    for row in rows:
        address = row[0]
        longitude = row[1]
        latitude = row[2]
        sold_price = "{:,}".format(row[3])
        bedroom = row[4]
        bathroom =row[5]
        sq_ft = row[6] 
        if sq_ft is None: 
            sq_ft = "---"
        else:
            sq_ft = "{:,}".format(row[6])
        days_on_market=row[7]

        entry = {}
        entry["address"] = address
        entry["longitude"] = longitude
        entry["latitude"] = latitude
        #Info Window
        entry["sold_price"] = sold_price
        entry["bedroom"] = bedroom
        entry["bathroom"] = bathroom
        entry["sq_ft"] = sq_ft
        entry["days_on_market"] = days_on_market

        output.append(entry)
    return jsonify(output)

@app.route('/bar')
def bar():
    conn = sqlite3.connect('sanfrancisco.db')

    c=conn.cursor()
    c.execute("SELECT Location, AVG(Sold_Price) AS AVG_Sold_Price FROM Address GROUP BY Location ORDER BY AVG_Sold_Price DESC")

    rows=c.fetchall()
    output = {}

    x=[]
    y=[]

    for row in rows:
        Location = row[0]
        sold_price=row[1]

        # Ignore "San francisco"
        if Location.lower().find("san francisco") == 0:
            continue

        x.append(Location)
        y.append(sold_price)    

    output["x"] = x
    output["y"] = y

    return jsonify(output)
   
# Over asking %

@app.route('/percentage')
def percentage():
    conn = sqlite3.connect('sanfrancisco.db')

    c=conn.cursor()
    c.execute("SELECT Location, SUM(Sold_Price), SUM(Original_Price), COUNT(Location) FROM Address WHERE Original_Price > 0 GROUP BY Location")

    rows=c.fetchall()
    output = {}

    x=[]
    y=[]

    for row in rows:
        Location = row[0]
        sold_price=row[1]
        original_price = row[2]
        count = row[3]

        # Ignore "San francisco"
        if Location.lower().find("san francisco") == 0:
            continue

        x.append(Location)
        avg_percentage = (sold_price - original_price)/original_price
        y.append(avg_percentage * 100)    

    output["x"] = x
    output["y"] = y

    return jsonify(output)
      

if __name__ == "__main__":
    app.run(debug=True)

