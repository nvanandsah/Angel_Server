from flask import Flask, json, request, render_template, jsonify
import sqlite3
import datetime
import time
app = Flask(__name__)
try:
    conn = sqlite3.connect('connection.db')
    conn.execute('CREATE TABLE data2 (timestamp TEXT, json_Dump TEXT)')
    conn.close()
except Exception:
    pass

@app.route('/store/<st>')
def hello_world(st = None):
    with sqlite3.connect("connection.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO data (timestamp,json_dump) VALUES (?,?)",(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') ,st))
        con.commit()
#        con.close()
    return json.dumps(st)


@app.route('/get')
def getr():
    con = sqlite3.connect("connection.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data")
    rows = cur.fetchall();
    return render_template("index.html",rows = rows)


@app.route('/getjson')
def getjson(data=None):
    data = []
    con = sqlite3.connect("connection.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data")
    rows = cur.fetchall();
    for row in rows:
        data.append([x for x in row])
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0 ', port='80')
