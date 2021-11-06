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

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/401')
    def access_denied():
        return render_template('401.html')

    @app.route('/404')
    def page_not_found():
        return render_template('404.html')

    @app.route('/500')
    def server_error():
        return render_template('500.html')

    @app.route('/table')
    def table():
        return render_template('table.html')

    @app.route('/login',methods=['GET', 'POST'])
    def login():
        return render_template('login.html')

    @app.route('/passwordreset',methods=['GET', 'POST'])
    def passwordreset():
        return render_template('passwordreset.html')

    if __name__ == "__main__":
        app.run()
