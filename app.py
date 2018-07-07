from flask import Flask, json, request, render_template, jsonify
import sqlite3
app = Flask(__name__)
try:
    conn = sqlite3.connect('connection.db')
    conn.execute('CREATE TABLE data (timestamp TEXT, json_Dump TEXT)')
    conn.close()
except Exception:
    pass

@app.route('/store/<st>')
def hello_world(st = None):
    res = st.split(",");
    timestamp = res[0]
    res = res[1:]
    res3 = {}
    del res[1::2]
    for i in res:
        res3[i] = st.count(i)
    with sqlite3.connect("connection.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO data (timestamp,json_dump) VALUES (?,?)",(timestamp ,json.dumps(res3)))
        con.commit()
#        con.close()
    return json.dumps(res3)


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
    app.run()
