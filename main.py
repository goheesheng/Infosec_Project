from flask import Flask, render_template, g
import sqlite3
import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof = 100)

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

blockchain = Blockchain()



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

    @app.route('/homepage')
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

    @app.route('/',methods=['GET', 'POST'])
    def login():
        return render_template('login.html')

    @app.route('/passwordreset',methods=['GET', 'POST'])
    def passwordreset():
        return render_template('passwordreset.html')

    @app.route('/submission',methods=['GET', 'POST'])
    def submission():
        return render_template('submission.html')

    @app.route('/verification')
    def verification():
        return render_template('verification.html')

    @app.route('/charts')
    def charts():
        return render_template('charts.html')

    @app.route('/tables')
    def tables():
        return render_template('table.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    if __name__ == "__main__":
        app.run()
