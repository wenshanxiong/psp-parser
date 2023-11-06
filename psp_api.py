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
            return "<p>That ain't a date I reckon. Gimme YYYY-MM-DD</p>", 400
    elif start and end:
        if validate_date(start) and validate_date(end):
            return jsonify(queries.get_price_by_date(cur, start, end))
        else:
            return "<p>That ain't a date I reckon. Gimme YYYY-MM-DD</p>", 400
    else:
        return """
        <p>Where the date at dude??</p>
        <p>Only /psp?date=[YYYY-MM-DD] or /psp?start=[YYYY-MM-DD]&end=[YYYY-MM-DD] accepted.</p>
        """, 400
        
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return """
    <p>Sneaky sneaky.</p>
    <p>Only /psp?date=[YYYY-MM-DD] or /psp?start=[YYYY-MM-DD]&end=[YYYY-MM-DD] accepted.</p>
    """, 400

  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=6969, help="API port number")
    parser.add_argument("-d", "--debug", default=False, help="Run flask in debug mode", action="store_true")
    args = parser.parse_args()
    app.run(host="0.0.0.0", debug=args.debug, port=args.port)