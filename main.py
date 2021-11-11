import shelve
import hashlib
from flask import Flask, request, render_template, g
from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import StringField, SubmitField, validators
import sqlite3
import hashlib
import json
from time import time
from forms import File_submit

class FileSubmit(FlaskForm):
    sender = StringField("Sender",[validators.Length(min=1, max=400), validators.DataRequired()] )
    recipient = StringField("Recipient",[validators.Length(min=1, max=400), validators.DataRequired()] )
    submission = FileField("Submission" )
    submit = SubmitField("Submit")



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="hashhashhashhashhashhashhashhashhashhashhashhashhashhashhash", proof = 100)

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

    def new_transaction(self, sender, recipient, hashval):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'hash': hashval
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
app.config['SECRET_KEY'] = "secret key"
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
        file_submit = FileSubmit()
        if request.method == "POST":
            z=file_submit.submission.data.filename
            file_submit.submission.data.save(z)
            file = open(file_submit.submission.data.filename)
            readFile = file.read()
            md5Hash = hashlib.md5(readFile.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            transaction = blockchain.new_transaction(file_submit.recipient.data, file_submit.sender.data, md5Hashed)
            blockchain.new_block('123')
            return render_template('test.html',chain = blockchain.chain)
        return render_template('submission.html',form = file_submit)

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
