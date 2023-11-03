import datetime
import sqlite3
from flask import Flask, request, jsonify
from queries import PSP_DB
import queries

app = Flask(__name__)
con = sqlite3.connect(PSP_DB, check_same_thread=False)
cur = con.cursor()

def validate_date(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False

@app.route('/psp') 
def query_example():
    date = request.args.get('date')
    start = request.args.get('start')
    end = request.args.get('end')
    if date:
        if validate_date(date):
            return jsonify(queries.get_price_by_date(cur, date, date))
        else:
            return "<p>That ain't a date I reckon. Gimme YYYY-MM-DD</p>"
    elif start and end:
        if validate_date(start) and validate_date(end):
            return jsonify(queries.get_price_by_date(cur, start, end))
        else:
            return "<p>That ain't a date I reckon. Gimme YYYY-MM-DD</p>"

  
if __name__ == '__main__': 
    app.run(debug=True, port=5000)

# bids?start=01-01-2012&end=01-31-2012