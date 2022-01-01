import os

from cs50 import SQL
from flask import Flask ,g

app = Flask(__name__)



def connect_db():
    sql =sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql
    
def get_db():
    if not hasattr(g,'sqlite3'):
        g.sqlite3_db= connect_db()
    return g.sqlite3_db
        
@app.teardown_appcontext
def close_db(error):
    if  hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return '<h1> Hello,world!<h1>'


@app.route('/users')
def viewusers():
    db = get_db()
    cursor = db.execute('SELECT id, name,age FROM users')
    results = cursor.fetchall()
    return f"<h1> The Id is {results[0][id]}. <br> The Name is {results[0][name]}. <br> age is {result[0][age]}. <br>"
    



if __name__ =='__main__':
    app.run(debug= True)