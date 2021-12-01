
import hashlib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, g, redirect, url_for, flash
import pyotp
from cryptography.fernet import Fernet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import smtplib
from wtforms import StringField, SubmitField, validators
import sqlite3
import hashlib
import json
import bcrypt
from time import time
from forms import FileSubmit, Login_form, Otp, Register
import random
import pyodbc
import textwrap
from mssql_auth import database, server

context = ssl.create_default_context()
sender = "IT2566proj@gmail.com"
senderpass = 'FishNugget123'
salt = bcrypt.gensalt()
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
    SERVER=' + server + '; \
    DATABASE=' + database + ';\
    Trusted_Connection=yes;'
)
insert_query = textwrap.dedent('''
    INSERT INTO user_login (username, first_name, last_name, pass_hash, otp_code,email) 
    VALUES (?, ?, ?, ?, ?, ?);
''')

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="hashhashhashhashhashhashhashhashhashhashhashhashhashhashhash", proof=100)

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
        if not hasattr(g, 'sqlite3'):  # checks if there is a database already connected
            g.sqlite3_db = connect_db()
        return g.sqlite3_db


    # test code to access db
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


    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')


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


    @app.route('/', methods=['GET', 'POST'])
    def login():
        login_form = Login_form()
        if request.method == "POST":
            email = login_form.email.data
            password = login_form.email.data
            PassHash = hashlib.md5(password.encode("utf-8"))
            PassHashed = PassHash.hexdigest()
            # Insert MSSQL to check email and password
            if True:
                return redirect(url_for("otpvalidation"))
        return render_template('login.html', form=login_form)


    @app.route('/validation')
    def otpvalidation():
        return render_template("loginotp.html")


    @app.route("/validation", methods=["POST"])
    def otpvalidation2():
        # retrive encrypted key
        # decrypt with user password
        gen_otp = pyotp.random_base32()
        secret_example = '6HDZKEGUIHTZLF35LPKKOX56XYGHUF7E'

        # getting OTP provided by user
        otp = int(request.form.get("otp"))

        # verifying submitted OTP with PyOTP
        if pyotp.TOTP(secret).verify(otp):
            # inform users if OTP is valid
            return redirect(url_for("homepage"))
        else:
            # inform users if OTP is invalid
            flash("You have supplied an invalid 2FA token!", "danger")
            return redirect(url_for("login"))


    @app.route('/passwordreset', methods=['GET', 'POST'])
    def passwordreset():
        return render_template('passwordreset.html')


    @app.route('/submission', methods=['GET', 'POST'])
    def submission():
        file_submit = FileSubmit()
        if request.method == "POST":
            z = file_submit.submission.data.filename
            file_submit.submission.data.save(z)
            file = open(file_submit.submission.data.filename)
            readFile = file.read()
            md5Hash = hashlib.md5(readFile.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            transaction = blockchain.new_transaction(file_submit.recipient.data, file_submit.sender.data, md5Hashed)
            blockchain.new_block('123')
            return render_template('test.html', chain=blockchain.chain)
        return render_template('submission.html', form=file_submit)


    @app.route('/verification')
    def verification():
        return render_template('verification.html')


    @app.route('/charts')
    def charts():
        return render_template('charts.html')


    @app.route('/tables')
    def tables():
        return render_template('table.html')


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        register = Register()
        if request.method == "POST":
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                DATABASE=' + database + ';\
                Trusted_Connection=yes;'
            )
            username = register.username.data
            firstname = register.firstname.data
            lastname = register.lastname.data
            email = register.email.data
            md5Hash = hashlib.md5(register.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            otp_code = pyotp.random_base32()
            values = (username, firstname, lastname, md5Hashed, otp_code, email)
            cursor = cnxn.cursor()
            cursor.execute('SELECT username, email FROM user_login')
            for x in cursor:
                if x.username == username or x.email == email:
                    return render_template('exists.html')
            cursor.execute(insert_query, values)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            return render_template('displayotp.html', otp=otp_code)

        return render_template('register.html', form=register)


    if __name__ == "__main__":
        app.run()
