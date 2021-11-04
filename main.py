from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
with app.app_context():

    def connect_db():
        con = sqlite3.connect('patient.db')
        con.row_factory = sqlite3.Row
        return con

    def get_db():
        if not hasattr(g, 'sqlite3'):  #checks if there is a database already connected
            g.sqlite3_db = connect_db()
        return g.sqlite3_db


    #test code to access db
    db = get_db()
    cursor = db.execute('select * from patient')
    results = cursor.fetchall()
    db.close()
    for result in results:
        for i in result:
            print(i)

    @app.route('/main',methods=['GET', 'POST'])
    def main():
        return render_template('helloworld.html')

    if __name__ == "__main__":
        app.run()
