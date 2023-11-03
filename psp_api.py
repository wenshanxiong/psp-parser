import datetime
import sqlite3
import queries
import argparse
from flask import Flask, request, jsonify
from queries import PSP_DB

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
def query_psp():
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
    else:
        return """
        <p>Where the date at dude??</p>
        <p>Only /psp?date=[date] or /psp?start=[start_date]&end=[end_date] allowed.</p>
        """
        
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return """
    <p>Sneaky sneaky.</p>
    <p>Only /psp?date=[date] or /psp?start=[start_date]&end=[end_date] allowed.</p>
    """

  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=6969, help="Parse tomorrow's prices")
    args = parser.parse_args()
    app.run(debug=True, port=args.port)