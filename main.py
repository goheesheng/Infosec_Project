
import hashlib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, g, redirect, url_for, flash, session
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
from functools import wraps
import random
import pyodbc
import textwrap
from mssql_auth import database, server
from flask_qrcode import QRcode

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
    INSERT INTO users (username, first_name, last_name, pass_hash, otp_code,email) 
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
QRcode(app)
app.config['SECRET_KEY'] = "secret key"
def login_required(requireslogin):
    @wraps(requireslogin)
    def decorated_func(*args, **kwargs):
        if "access" not in session: #No session info or user not in db
            flash("Invalid User")
            return redirect(url_for('login'))
        else:
            return requireslogin(*args, **kwargs)
    return decorated_func

def researcher_needed(needresearcher):
    @wraps(needresearcher)
    def decorated_func(*args, **kwargs):
        if session['access'] != '0':
            flash("Invalid User")
            return redirect(url_for('home'))
        else:
            return needresearcher(*args, **kwargs)
    return decorated_func

def patient_needed(needpatient):
    @wraps(needpatient)
    def decorated_func(*args, **kwargs):
        if session['access'] != '1':
            flash("Invalid User")
            return redirect(url_for('home'))
        else:
            return needpatient(*args, **kwargs)
    return decorated_func

def doctor_needed(needdoctor):
    @wraps(needdoctor)
    def decorated_func(*args, **kwargs):
        if session['access'] != '2':
            flash("Invalid User")
            return redirect(url_for('home'))
        else:
            return needdoctor(*args, **kwargs)
    return decorated_func


def admin_needed(needadmin):
    @wraps(needadmin)
    def decorated_func(*args, **kwargs):
        if session['access'] < '3':
            flash("Invalid User")
            return redirect(url_for('home'))
        else:
            return needadmin(*args, **kwargs)
    return decorated_func

def head_admin_needed(needhadmin):
    @wraps(needhadmin)
    def decorated_func(*args, **kwargs):
        if session['access'] < '4':
            flash("Invalid User")
            return redirect(url_for('home'))
        else:
            return needhadmin(*args, **kwargs)
    return decorated_func

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
    @login_required
    def homepage():
        return render_template('homepage.html')


    @app.route('/dashboard')
    @login_required
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
    @login_required
    def table():
        return render_template('table.html')


    @app.route('/', methods=['GET', 'POST'])
    def login():
        login_form = Login_form()
        if request.method == "POST":
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                            DATABASE=' + database + ';\
                            Trusted_Connection=yes;'
            )
            email = login_form.email.data
            password = login_form.password.data
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            cursor = cnxn.cursor()
            user_id = cursor.execute("select user_id from users where email=\'"+email+"\' and pass_hash=\'"+md5Hashed+"\'").fetchval()
            if user_id:
                session['user_id'] = user_id
                cursor.close()
                cnxn.close()
                return redirect(url_for("otpvalidation"))
            else:
                cursor.close()
                cnxn.close()
                return render_template("404.html")
        return render_template('login.html', form=login_form)


    @app.route('/validation')

    def otpvalidation():
        return render_template("loginotp.html")


    @app.route("/validation", methods=["POST"])

    def otpvalidation2():
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
            SERVER=' + server + '; \
                                    DATABASE=' + database + ';\
                                    Trusted_Connection=yes;'
        )
        cursor = cnxn.cursor()
        otp_seed = cursor.execute("select otp_code from users where user_id=\'"+str(session['user_id'])+"\'").fetchval()


        # getting OTP provided by user
        otp = int(request.form.get("otp"))

        # verifying submitted OTP with PyOTP
        if pyotp.TOTP(otp_seed).verify(otp):
            info = cursor.execute("select username, first_name, last_name, user_access_level  from users where otp_code=\'"+str(otp_seed)+"\'").fetchall()
            (username,first_name,last_name,access_level) = info[0]
            session['username'] = username
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['access'] = access_level
            cursor.close()
            cnxn.close()
            if access_level == 0:
                return redirect(url_for("homepage"))
            elif access_level == 1:
                return redirect(url_for('dashboard'))
            elif access_level == 2:
                return redirect(url_for('dashboard'))
            elif access_level == 3:
                return redirect(url_for('dashboard'))
        else:
            print("wrong")
            cursor.close()
            cnxn.close()
            return redirect(url_for("login"))


    @app.route('/passwordreset', methods=['GET', 'POST'])
    @login_required
    def passwordreset():
        return render_template('passwordreset.html')


    @app.route('/submission', methods=['GET', 'POST'])
    @login_required
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
    @login_required
    def verification():
        return render_template('verification.html')


    @app.route('/charts')
    @login_required
    def charts():
        return render_template('charts.html')


    @app.route('/tables')
    @login_required
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
            cursor.execute('SELECT username, email FROM users')
            for x in cursor:
                if x.username == username or x.email == email:
                    return render_template('exists.html')
            cursor.execute(insert_query, values)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            qr = 'otpauth://totp/AngelHealth:'+username+'?secret='+otp_code
            return render_template('displayotp.html', otp=otp_code, qrotp=qr)

        return render_template('register.html', form=register)


    if __name__ == "__main__":
        app.run()
