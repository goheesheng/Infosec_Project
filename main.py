import hashlib
import ssl
import pyqrcode
from docx import Document
from docxcompose.composer import Composer
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mobility import Mobility
import os
from datetime import *
from flask import Flask, request, render_template, g, redirect, url_for, flash, session,send_from_directory
import pyotp
import os
import smtplib
import hashlib
import re
import random
import bcrypt
from forms import FileSubmit, Patient_Login_form, Admin_Login_form,Otp, Register, RequestPatientInfo_Form, Appointment, RegisterDoctor, RegisterResearcher, RegisterHr
from functools import wraps
import pyodbc
import textwrap
from mssql_auth import database, server
from flask_qrcode import QRcode
from datetime import datetime

context = ssl.create_default_context()

salt = bcrypt.gensalt()
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
    SERVER=' + server + '; \
    DATABASE=' + database + ';\
    Trusted_Connection=yes;'
)


# dont u touch u gay boi
# class Blockchain(object):
#     def __init__(self):
#         self.chain = []
#         self.pending_transactions = []
#         self.new_block(previous_hash="hashhashhashhashhashhashhashhashhashhashhashhashhashhashhash", proof=100)

#     def new_block(self, proof, previous_hash=None):
#         block = {
#             "index": len(self.chain) + 1,
#             'timestamp': time(),
#             'transactions': self.pending_transactions,
#             'proof': proof,
#             'previous_hash': previous_hash or self.hash(self.chain[-1]),
#         }
#         self.pending_transactions = []
#         self.chain.append(block)

#         return block

#     @property
#     def last_block(self):
#         return self.chain[-1]

#     def new_transaction(self, sender, recipient, hashval):
#         transaction = {
#             'sender': sender,
#             'recipient': recipient,
#             'hash': hashval
#         }
#         self.pending_transactions.append(transaction)
#         return self.last_block['index'] + 1

#     def hash(self, block):
#         string_object = json.dumps(block, sort_keys=True)
#         block_string = string_object.encode()

#         raw_hash = hashlib.sha256(block_string)
#         hex_hash = raw_hash.hexdigest()

#         return hex_hash


# blockchain = Blockchain()


app = Flask(__name__)
QRcode(app)
app.config['SECRET_KEY'] = "secret key"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'saved')


# def login_required(requireslogin):
#     @wraps(requireslogin)
#     def decorated_func(*args, **kwargs):
#         if "access" not in session:  # No session info or user not in db
#             flash("Invalid User")
#             return redirect(url_for('login'))
#         else:
#             return requireslogin(*args, **kwargs)

#     return decorated_func



def custom_login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        # print(session['login'],'wrapper')
        if session is None:
            return redirect(url_for('login'))
# fix this later ES

        if 'expirydate' in app.config:
            if app.config['expirydate']<= datetime.utcnow():
                flash('session expired','warning')
                app.config['expirydate']=None
                return redirect(url_for('login'))


        # if session.get('csrf_token') is None:
        #     print('session modifed')
        #     ipaddress=request.remote_addr
        #     try:
        #         if app.config['lastusername'] is not None:
        #             filter=cookieFilter(ipaddress,app.config['lastusername'])
        #         else:
        #             filter = cookieFilter(ipaddress)
        #         serializationlogger.addFilter(filter)
        #         serializationlogger.warning('Cookie has been modified')
        #         return redirect(url_for('login'))
        #     except:
        #         pass

        if 'login' not in session or session['login']!=True:
            flash("Please log in to access this page","warning")
            return redirect(url_for('login'))


        print(session['login'],'wrapper session logged in')

        return f(*args,**kwargs)

    return wrap


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

def allowed_filename(filename):
    expression=re.compile(r"(?i)^[\w]*(.docx)$")
    return re.fullmatch(expression,filename)

def check_file_hash(file_name,stored_hash):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name),"rb") as original_file:
        md5Hash = hashlib.md5(original_file.read())
        fileHashed = md5Hash.hexdigest()
        return fileHashed==stored_hash

def get_file_data_from_database(patient_id):
    cursor = cnxn.cursor()
    data = cursor.execute("select * from patient_file where patient_id=?",(patient_id)).fetchone()
    cursor.close()
    return data



@app.context_processor
def inject_templates_with_session_date():
    return dict(session)

with app.app_context():
    @app.route('/homepage')
    @custom_login_required
    def homepage():
        flash("welcome")
        return render_template('homepage.html')

    @app.route('/')
    def index():
        session.clear()
        return render_template('index.html')

    @app.route('/dashboard')
    @custom_login_required
    def dashboard():
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
            SERVER=' + server + '; \
                                    DATABASE=' + database + ';\
                                    Trusted_Connection=yes;'
        )
        cursor = cnxn.cursor()
        patients = cursor.execute("SELECT * FROM patients").fetchall()
        doctors = cursor.execute("SELECT * FROM doctors").fetchall()
        hr = cursor.execute("SELECT * FROM hr").fetchall()
        researcher = cursor.execute("SELECT * FROM researchers").fetchall()
        return render_template('dashboard.html', patients=patients, doctors=doctors, hrs=hr, researchers=researcher)


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
    @custom_login_required
    def table():
        return render_template('table.html')

    def SendMail(ImgFileName, email,topic):
        with open(ImgFileName, 'rb') as f:
            img_data = f.read()
        sender = "IT2566proj@gmail.com"
        senderpass = 'FishNugget123'
        msg = MIMEMultipart()
        msg['Subject'] = topic+' Qr Code For Google Authenticator'
        msg['From'] = 'AngelHealth@mail.gov.sg'
        msg['To'] = email

        text = MIMEText("test")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
        msg.attach(image)

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(sender, senderpass)
        s.sendmail(sender, email, msg.as_string())
        s.quit()


    def add_admin():
        while True:
            key = input("Do you want to create Head Admin ID and password? (Y/N/Show/Delete)").capitalize()
            if key == "Y":
                pattern = ('^\d{6}[A-Za-z]$')
                username = input("Enter New Head Admin ID: ")
                result = re.match(pattern,username)
                while result == None:
                    print("Only first 6 digits and 1 alphabet at the end!")
                    username = input("Enter New Head Admin ID: ")
                    result = re.match(pattern,username)
                cursor = cnxn.cursor()

                check = cursor.execute("SELECT username FROM head_admin WHERE username = ?",
                                       (username)).fetchval()  # prevent sql injection

                firstname = input("Enter New Head Admin First Name: ")
                lastname = input("Enter New Head Admin last Name: ")
                email = input("Enter New Head Admin email: ")

                pattern = ('^(?=\S{10,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
                admin_password = input("Enter New Head Admin Password: ")

                result = re.match(pattern,admin_password)
                while result == None:
                    print( "Password must contain 10-20 characters, number, uppercase, lowercase, special character.")
                    admin_password = input("Enter New Head Admin Password: ")
                    result = re.match(pattern,admin_password)
                phone_no = input("Enter New Head Admin Phone Number: ")
                
                otp_code = pyotp.random_base32()

                md5Hash = hashlib.md5(admin_password.encode("utf-8"))
                md5Hashed = md5Hash.hexdigest()
                address = input("Enter New Head Admin address: ")
                postal_code = input("Enter New Head Admin postal code: ")

                cursor = cnxn.cursor()
                check_username = cursor.execute("SELECT username FROM head_admin WHERE username = ?",
                                       (username)).fetchval()  # prevent sql injection
                check_email = cursor.execute("SELECT email FROM head_admin WHERE email = ?",
                                       (email)).fetchval()  # prevent sql injection

                if check_email == None and check_username == None :
                    insert_query = "INSERT INTO head_admin (username, first_name, last_name, pass_hash,email,otp_code,phone_no,access_level,postal_code,address) \
                            VALUES (?, ?, ?, ?, ?, ?,?,?,?,?); "
                    values = (username, firstname, lastname, md5Hashed,
                              email,otp_code,phone_no,'head_admin',address,postal_code)
                    cursor.execute(insert_query, values)
                    cursor.commit()
                    cursor.close()
                    cursor = cnxn.cursor()
                    insert_query = "INSERT INTO access_list (username,access_level,pass_hash) \
                            VALUES (?, ?,?); "
                    values = (username,'head_admin',md5Hashed)
                    cursor.execute(insert_query, values)
                    cursor.commit()
                    cursor.close()
                    print('Sending email OTP...')
                    qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                    image = pyqrcode.create(qr)
                    image.png('image.png', scale=5)
                    SendMail("image.png", email, "Head Admin")
                    os.remove('image.png')
                    print('Successful creating Head Admin')
                    cursor = cnxn.cursor()
                    check = cursor.execute("SELECT * FROM head_admin").fetchall()  # prevent sql injection
                    print("List of Head Admins:")
                    for x in check:
                        username = x.username.strip()
                        first_name = x.first_name.strip()
                        last_name = x.last_name.strip()
                        email = x.email.strip()
                        phone_no = x.phone_no.strip()
                        print(f"Username: {username}, First Name: {first_name}, Last Name: {last_name}, Email: {email}, Phone No: {phone_no}")
                    continue
                else:
                    print("Head Admin already exists! Check your username and email!!!!")
      
            elif key == "N":
                break
            elif key == "Show":
                cursor = cnxn.cursor()
                check = cursor.execute("SELECT * FROM head_admin").fetchall()  # prevent sql injection
                print("List of Head Admins:")
                for x in check:
                    username = x.username.strip()
                    first_name = x.first_name.strip()
                    last_name = x.last_name.strip()
                    email = x.email.strip()
                    print(f"Username: {username}, First Name: {first_name}, Last Name: {last_name}, Email: {email}")

                cursor.close()
            elif key == 'Delete':
                # try:
                cursor = cnxn.cursor()
                key = input("Enter the Head Admin ID to delete: ")
                check = cursor.execute("SELECT * FROM head_admin WHERE username = ?",
                                       (key)).fetchval()  # prevent sql injection
                if check == None:
                    print("Head admin does not exist")
                    continue

                else:
                    check = cursor.execute("DELETE FROM head_admin WHERE username = ?", (key))  # prevent sql injection
                    cursor.commit()
                    check = cursor.execute("DELETE FROM access_list WHERE username = ?", (key))  # prevent sql injection
                    cursor.commit()
                    print(f"{key} was removed as Head Admin.")
                    check = cursor.execute("SELECT * FROM head_admin").fetchall()  # prevent sql injection
                    print("List of Head Admins:")
                    for x in check:
                        username = x.username.strip()
                        first_name = x.first_name.strip()
                        last_name = x.last_name.strip()
                        email = x.email.strip()
                        print(f"Username: {username}, First Name: {first_name}, Last Name: {last_name}, Email: {email}")
                    cursor.close()


            # except:
            #     print('Error in deleting Head Admin in MSSQL Database')
            else:
                print("Please enter Y or N or Delete only!")
                continue

    # must add get method to to retrieve url
    @app.route("/viewUser", methods=["GET", "POST"])
    def viewUser():
        if request.method == 'GET':
            print(session)
            return render_template("customerDetail.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        patient_login_form = Patient_Login_form(request.form)
        admin_login_form = Admin_Login_form(request.form)
        # session['patient_id'] = None
        # session['researcher_id'] = None
        # session['doctor_id'] = None
        # session['admin_id'] = None
        # session['head_admin_id'] = None
        # session['otp-semi-login'] = None # used to prevent attacker direct traversal to /validation url
        if patient_login_form.patient_submit.data and patient_login_form.validate():
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                                DATABASE=' + database + ';\
                                Trusted_Connection=yes;'
            )
            passed = False
            username = patient_login_form.username.data
            password = patient_login_form.password.data
            print(username,password)
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            print(md5Hashed)
            cursor = cnxn.cursor()
            user_info = cursor.execute(
                "select * from patients where username = ? and pass_hash = ?",
                (username, md5Hashed)).fetchone() #fetchone() dont delete this except others
            print(user_info,'user_id')
            print(cursor,'cursor')
            # for reference list index!
            # /****** Script for SelectTopNRows command from SSMS  ******/
            # SELECT TOP (1000) [patient_id] 0
            #     ,[username] 1
            #     ,[first_name]2
            #     ,[last_name]3
            #     ,[pass_hash]4
            #     ,[otp_code]5
            #     ,[email]6
            #     ,[phone_no]7
            #     ,[address]8
            #     ,[postal_code]9
            #     ,[hospital]10
            #     ,[tending_physician]11
            #     ,[appointment]12
            #     ,[access_level]13
            # FROM [database1].[dbo].[patients]
            if user_info != None:
            #     #alternative way
            #     access_list = {'patient': 'patients', 'doctor': 'doctors', 'researcher': 'researchers', 'hr': 'hr','head_admin': 'head_admin'}
            #     if user_info[0] in access_list:
            #         col_name_query=f"select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = {access_list[user_info]};"
            #         print(col_name_query)
            #         col_names = cursor.execute(col_name_query)
            #         for count,col_name in enumerate(col_names):
            #             if type(user_info)==str:
            #                 session[col_name]=user_info[count].strip()
            #             else:
            #                 session[col_name]=user_info[count]
            #
                passed = True
                print(user_info[0],'id')
                print(user_info[1].strip(),'id')
                print(user_info[3].strip(),'id')
                print(user_info[4].strip(),'id')
                print(user_info[7],'id')
                session['id'] = user_info[0]
                session['username'] = user_info[1].strip()
                session['first_name'] = user_info[2].strip()
                session['last_name'] = user_info[3].strip()
                session['phone_no'] =  user_info[7]
                session['email'] =  user_info[6].strip()
                session['address'] =  user_info[8].strip()
                session['postal_code'] =  user_info[9]
                session['access_level'] = user_info[13].strip()

                # should we add this too? as session?
                try:# if it is not None then  user_info[3]
                    session['tending_physician'] = user_info[11].strip()
                except:
                    session['tending_physician'] = None
                try:# if it is tending_physician None then strip
                    session['appointment'] = user_info[12].strip()
                except:
                    session['appointment'] =  None
                
                cursor.close()
                session['otp-semi-login'] = True
                print('user logged in')
                flash("Please continue with otp validation before login is successful","success")
                return redirect(url_for("otpvalidation"))
            else:
                cursor.close()
                print("ERROR")
                flash("Invalid username or password","error")
                return redirect(url_for('login'))

        elif admin_login_form.staff_submit.data and admin_login_form.validate():
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                                DATABASE=' + database + ';\
                                Trusted_Connection=yes;'
            )
            passed = False
            username = admin_login_form.username.data
            password = admin_login_form.password.data
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            cursor = cnxn.cursor()
            access_info = cursor.execute(
                "select * from access_list where username = ? and pass_hash = ?",
                (username, md5Hashed)).fetchone() #fetchone() dont delete this except others
            cursor = cnxn.close()


            # doctorCheck = cursor.execute("select * from doctors where username = ? and pass_hash = ?",
            #                              (username, md5Hashed)).fetchone()
            # for x in cursor:
            #     print(x)
            #     name = x.username.strip()
            #     patient_id = x.patient_id #is integer so apparently dont need strip? 
            #     first_name = x.first_name.strip()
            #     last_name = x.last_name.strip()
            #     email = x.email.strip()
            #     address = x.address.strip()
            #     postal_code = x.postal_code.strip()
            #     try:# if it is not None then strip
            #         tending_physician = x.tending_physician.strip() 
            #     except:
            #         tending_physician = x.tending_physician
            #     try:# if it is not None then strip
            #         appointment = x.appointment.strip()
            #     except:
            #        appointment = x.appointment

            # researcherCheck = cursor.execute("select * from researchers where username = ? and pass_hash = ?",
            #                                  (username, md5Hashed)).fetchone()
            # adminCheck = cursor.execute("select * from hr where username = ? and pass_hash = ?",
            #                             (username, md5Hashed)).fetchone()
            # headadminCheck = cursor.execute("select * from head_admin where username = ? and pass_hash = ?",
                                            # (username, md5Hashed)).fetchone()

            #added md5Hashed password in access_list table so to user username and hashed password for checking if it is in both access_list table and unqiue role tables

            #check whether in access list table
            if access_info != None:
                cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                                DATABASE=' + database + ';\
                                Trusted_Connection=yes;'
            )
                # session['username'] = access_info[0].strip()
                # session['access_list'] = access_info[1].strip()
                access_level_username = access_info[0].strip()
                access_level_access_list = access_info[1].strip()
                print(access_level_username,'username')
                print(access_level_access_list)
                #check whether was it created in the individual tables (e.g. is it in doctors or researchers or HR or head_admin tables?)
                cursor = cnxn.cursor()
                #Retrieve the unique roles using access_level_access_list
                if access_level_access_list == "researchers":
                    user_info = cursor.execute(
                    f"select * from {access_level_access_list} where username = ? and pass_hash = ?",
                    (access_level_username, md5Hashed)).fetchone() #fetchone() dont delete this except others
                    cursor = cnxn.close()
                    # CREATE TABLE [dbo].[researchers](
                    #     [username] [nchar](30) NOT NULL,0
                    #     [first_name] [nchar](30) NOT NULL,1
                    #     [last_name] [nchar](30) NOT NULL,2
                    #     [pass_hash] [varchar](50) NOT NULL,3
                    #     [otp_code] [varchar](50) NOT NULL,4
                    #     [email] [varchar](50) NOT NULL,5
                    #     [phone_no] [varchar](20) NOT NULL,6
                    #     [address] [varchar](50) NOT NULL,7
                    #     [postal_code] [varchar](6) NOT NULL,8
                    #     [company] [varchar](50) NULL,9
                    #     [researcher_id] [int] IDENTITY(1,1) NOT NULL,10
                    #     [access_level][varchar](30) NOT NULL 11
                    # ) ON [PRIMARY]
                    if user_info != None:
                        passed = True
                        print(user_info[10],'researcher_id')
                        print(user_info[0].strip(),'username')
                        print(user_info[2].strip(),'last_name')
                        print(user_info[6].strip(),'phone_no')
                        print(user_info[7].strip(),'address')
                        print(user_info[8].strip(),'postal_code')
                        print(user_info[11].strip(),'access_level')

                        session['id'] = user_info[10]
                        session['username'] = user_info[0].strip()
                        session['first_name'] = user_info[1].strip()
                        session['last_name'] = user_info[2].strip()
                        session['phone_no'] =  user_info[6].strip()
                        session['email'] =  user_info[5].strip()
                        session['address'] =  user_info[7].strip()
                        session['postal_code'] =  user_info[8].strip()
                        session['access_level'] =  user_info[11].strip()

                        # should we add this too? as session?
                        try:
                            session['company'] = user_info[9].strip() # If HR dk the company
                        except:
                            session['company'] = None
                elif access_level_access_list == "head_admin":
                    user_info = cursor.execute(
                    f"select * from {access_level_access_list} where username = ? and pass_hash = ?",
                    (access_level_username, md5Hashed)).fetchone() #fetchone() dont delete this except others
                    cursor = cnxn.close()
                        # CREATE TABLE [dbo].[head_admin](
                        # 	[head_admin_id] [int] IDENTITY(1,1) NOT NULL, 0
                        # 	[username] [nchar](30) NOT NULL,1
                        # 	[first_name] [nchar](30) NOT NULL,2
                        # 	[last_name] [nchar](30) NOT NULL,3
                        # 	[pass_hash] [varchar](50) NOT NULL,4
                        # 	[otp_code] [varchar](50) NOT NULL,5
                        # 	[email] [varchar](50) NOT NULL,6
                        # 	[phone_no] [varchar](20) NOT NULL,7
                        # 	[access_level][varchar](30) NOT NULL8
                        #   [postal_code][varchar](6) NOT NULL,9
	                    #   [address][varchar](50) NOT NULL10
                        # ) ON [PRIMARY]
                    if user_info != None:
                        passed = True
                        print(user_info[0],'id')
                        print(user_info[1].strip(),'username')
                        print(user_info[2].strip(),'first_name')
                        print(user_info[3].strip(),'last_name')
                        print(user_info[7].strip(),'phone_no')
                        print(user_info[6].strip(),'email')
                        print(user_info[10].strip(),'address')
                        print(user_info[9].strip(),'postal_code')
                        print(user_info[8].strip(),'access_level')

                        session['id'] = user_info[0]
                        session['username'] = user_info[1].strip()
                        session['first_name'] = user_info[2].strip()
                        session['last_name'] = user_info[3].strip()
                        session['phone_no'] =  user_info[7].strip()
                        session['email'] =  user_info[6].strip()
                        session['address'] =  user_info[10].strip()
                        session['postal_code'] =  user_info[9].strip()
                        session['access_level'] =  user_info[8].strip()
                        

                elif access_level_access_list == "hr":
                    user_info = cursor.execute(
                    f"select * from {access_level_access_list} where username = ? and pass_hash = ?",
                    (access_level_username, md5Hashed)).fetchone() #fetchone() dont delete this except others
                    cursor = cnxn.close()
                    # CREATE TABLE [dbo].[hr](
                    #     [hr_id] [int] IDENTITY(1,1) NOT NULL,0
                    #     [username] [nchar](10) NOT NULL,1
                    #     [first_name] [nchar](20) NOT NULL,2
                    #     [last_name] [nchar](20) NOT NULL,3
                    #     [pass_hash] [varchar](50) NOT NULL,4
                    #     [otp_code] [varchar](50) NOT NULL,5
                    #     [address] [varchar](50) NOT NULL,6
                    #     [postal_code] [varchar](6) NOT NULL,7
                    #     [email] [varchar](50) NOT NULL,8
                    #     [phone_no] [varchar](20) NOT NULL,9
                    #     [access_level][varchar](30) NOT NULL 10
                    # ) ON [PRIMARY]
                    if user_info != None:
                        passed = True
                        print(user_info[0],'id')
                        print(user_info[1].strip(),'username')
                        print(user_info[2].strip(),'first_name')
                        print(user_info[3].strip(),'last_name')
                        print(user_info[9].strip(),'phone_no')
                        print(user_info[8].strip(),'email')
                        print(user_info[6].strip(),'address')
                        print(user_info[7].strip(),'postal_code')
                        print(user_info[10].strip(),'access_level')

                        session['id'] = user_info[0]
                        session['username'] = user_info[1].strip()
                        session['first_name'] = user_info[2].strip()
                        session['last_name'] = user_info[3].strip()
                        session['phone_no'] =  user_info[9].strip()
                        session['email'] =  user_info[8].strip()
                        session['address'] =  user_info[6].strip()
                        session['postal_code'] =  user_info[7].strip()
                        session['access_level'] =  user_info[10].strip()

                elif access_level_access_list == "doctors":
                    user_info = cursor.execute(
                    f"select * from {access_level_access_list} where username = ? and pass_hash = ?",
                    (access_level_username, md5Hashed)).fetchone() #fetchone() dont delete this except others
                    cursor = cnxn.close()
                    # CREATE TABLE [dbo].[doctors](
                    #     [staff_id] [int] IDENTITY(1,1) NOT NULL,0
                    #     [username] [nchar](30) NOT NULL,1
                    #     [first_name] [nchar](30) NOT NULL,2
                    #     [last_name] [nchar](30) NOT NULL,3
                    #     [pass_hash] [varchar](50) NOT NULL,4
                    #     [otp_code] [varchar](50) NOT NULL,5
                    #     [email] [varchar](50) NOT NULL,6
                    #     [address] [varchar](50) NOT NULL,7
                    #     [postal_code] [varchar](6) NOT NULL,8
                    #     [department] [varchar](50) NOT NULL,9
                    #     [access_level][varchar](30) NOT NULL10
                    #     [phone_no] [varchar](20) NOT NULL11
                    # ) ON [PRIMARY]
                    if user_info != None:
                        passed = True
                        print(user_info[0],'id')
                        print(user_info[1].strip(),'username')
                        print(user_info[2].strip(),'first_name')
                        print(user_info[3].strip(),'last_name')
                        print(user_info[9].strip(),'phone_no')
                        print(user_info[8].strip(),'email')
                        print(user_info[6].strip(),'address')
                        print(user_info[7].strip(),'postal_code')
                        print(user_info[10].strip(),'access_level')

                        session['id'] = user_info[0]
                        session['username'] = user_info[1].strip()
                        session['first_name'] = user_info[2].strip()
                        session['last_name'] = user_info[3].strip()
                        session['phone_no'] =  user_info[11].strip()
                        session['email'] =  user_info[6].strip()
                        session['address'] =  user_info[7].strip()
                        session['postal_code'] =  user_info[8].strip()
                        session['access_level'] =  user_info[10].strip()

                        # should we add this too? as session?
                        try:
                            session['department'] = user_info[9].strip() # If HR dk the company
                        except:
                            session['department'] = None

           
            # if doctorCheck != None:
            #     user_type = "doctors"
            #     identifier = doctorCheck[0]
            # elif adminCheck != None:
            #     user_type = "admin"
            #     identifier = adminCheck[0]
            # elif researcherCheck != None:
            #     user_type = "researchers"
            #     identifier = researcherCheck[0]
            # elif headadminCheck != None:
            #     user_type = "head_admin"
            #     identifier = headadminCheck[0]
                else:
                    passed = False
                    return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)
            if passed:
                # session['id'] = identifier.strip() #need strip to remove the spaces
                # session[user_type] = username.strip()
                # print(session['id'],'idididid')
                # print(session['username'],'ididididnananananannana')
                # cursor.close()

                session['otp-semi-login'] = True
                return redirect(url_for("otpvalidation"))
            else:
                print('fail login')
                flash("Wrong username or password", "error")
                return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)
            # return render_template("404.html")

        else:
            return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)


    # @app.route('/validation')
    # # @custom_login_required
    # def otpvalidation():
    #     print("hello")
    #     return render_template("loginotp.html")


    @app.route("/validation", methods=["GET","POST"])
    def otpvalidation():
        cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                                DATABASE=' + database + ';\
                                Trusted_Connection=yes;'
        )
        if request.method=="POST":
            cursor = cnxn.cursor()
            print(session,'otpval check sess')
            if session['otp-semi-login'] and session['access_level'] == 'patient':
                # cursor.execute("select access_level from ")
                value =  session['username']

                (otp_seed, username, first_name, last_name) = cursor.execute(
                                    "select otp_code, username, first_name, last_name from patients where username = ?",
                                    (value)
                                ).fetchone()
            elif session['otp-semi-login'] and session['access_level'] == 'doctor':
                value =  session['username']

                (otp_seed, username, first_name, last_name) = cursor.execute(
                        "select otp_code, username, first_name, last_name from doctors where username = ?",
                        (value)
                    ).fetchone()[0]
            elif session['otp-semi-login'] and session['access_level'] == 'researcher':
                value =  session['username']

                (otp_seed, username, first_name, last_name) = cursor.execute(
                    "select otp_code, username, first_name, last_name from researchers where username = ?",
                    (value)
                ).fetchone()[0]
            elif session['otp-semi-login'] and session['access_level'] == 'hr':
                value =  session['username']
                (otp_seed, username, first_name, last_name) = cursor.execute(
                        "select otp_code, username, first_name, last_name from hr where username = ?",
                        (value)
                    ).fetchone()[0]
            elif session['otp-semi-login'] and session['access_level'] == 'head_admin':
                value =  session['username']
                print(value,'this is value')
                (otp_seed) = cursor.execute(
                    "select otp_code, username, first_name, last_name from head_admin where username = ?",
                    (value)).fetchone()[0]

            #PleaseNerfDictionary,
            # access_list={'patient':'patients','doctor':'doctors','researcher':'researchers','hr':'hr','head_admin':'head_admin'}
            # if session['access_level'] in access_list:
            #     query=f"select otp_code from {access_list[session['access_level']]} where username = ?"
            #     otp_seed=cursor.execute(query,(session['username'])).fetchone()[0]

            otp = int(request.form.get("otp"))
            print(otp_seed)
            print(pyotp.TOTP(otp_seed).now())
            # verifying submitted OTP with PyOTP
            if pyotp.TOTP(otp_seed).verify(otp):
                print("correct")
                session['login'] = True
                cursor.close()
                # session['login'] = True
                print(session['login'],'sslogin')
                print(session,'check sesison')

                return redirect(url_for('homepage'))
            else:
                print("wrong")
                cursor.close()
                flash("Wrong OTP", "error")
                return redirect(url_for("otpvalidation"))
            # else:
            #     print('false')
            #     flash('Wrong username or password!')
            #     return redirect(url_for("login"))
        if request.method == "GET":
            return render_template("loginotp.html")

    @app.route('/passwordreset', methods=['GET', 'POST'])
    @custom_login_required
    def passwordreset():
        return render_template('passwordreset.html')


    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()
        return redirect(url_for("login"))


    @app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
    def download(filename):
        #dpvalidationhere
        cursor= cnxn.cursor()
        if 'access_level' not in session:
            return redirect(request.referrer)
        else:
            tending_physician =cursor.execute("select tending_physician from patients where patient_id=?", (session['id'])).fetchone()[0]
            if session['username'] != tending_physician :
                flash("You unauthorized  to view this patients information")
                return redirect(request.referrer)

        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename)

    @app.route('/requestPatientInformation',methods=['GET','POST'])
    def requestPatientInformation():
        requestPatientInformationForm=RequestPatientInfo_Form(request.form)
        if request.method=='POST' :
            if requestPatientInformationForm.validate():
                patient_nric=requestPatientInformationForm.patient_nric.data
                cursor = cnxn.cursor()
                #Checking if patient exists in database with NRIC/USERNAME
                patient = cursor.execute("select * from patients where username=?",(patient_nric)).fetchone()
                if patient is not None:
                    retrieved = cursor.execute("select * from patient_file where patient_id=?", (patient[0])).fetchone()
                    if retrieved is None:
                        # Creating Base Document File for patient,insert file name,content,md5... into db
                        cursor = cnxn.cursor()
                        patient_name=f"{patient[2].strip()} {patient[3].strip()}"
                        insert_query = textwrap.dedent('''INSERT INTO patient_file  VALUES (?,?,?,?,?,?,?); ''')
                        newDocument=Document()
                        newDocument.add_heading(f"Medical record for {patient_name} with NRIC of {patient[1]}", 0)
                        newDocument.save(os.path.join(app.config['UPLOAD_FOLDER'],f"{patient[1].strip()}.docx"))
                        filecontent=open(os.path.join(app.config['UPLOAD_FOLDER'],f"{patient[1].strip()}.docx"),"rb").read()
                        md5Hash = hashlib.md5(filecontent)
                        fileHashed = md5Hash.hexdigest()
                        VALUES = (patient[0], f"{patient[1].strip()}.docx", filecontent,datetime.now().today().strftime("%m/%d/%Y, %H:%M:%S"),"Application",0,fileHashed)
                        cursor.execute(insert_query, VALUES)
                        cursor.commit()
                        cursor.close()
                    else:
                        file_name=retrieved[1]
                        file_content=retrieved[2]
                        stored_hash=retrieved[6]
                        if not(check_file_hash(file_name,stored_hash)):
                            with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name),"wb") as file_override:
                                file_override.write(file_content)
                    print(session,'here')
                    return redirect(url_for("submission", pid=patient[0]))

                cursor.close()
            flash("NRIC either does not exist or is invalid", "error")
            return redirect(url_for('requestPatientInformation'))

        if request.method=="GET" and session["access_level"] =="patient":
            return send_from_directory(directory=app.config['UPLOAD_FOLDER'],path=f"{session['username']}.docx")
        else:
            return render_template("requestPatientInformation.html",form=requestPatientInformationForm)

    @app.route('/submission/<pid>', methods=['GET', 'POST'])
    # @login_required
    def submission(pid):
        cursor = cnxn.cursor()
        if 'access_level' not in session:
            return redirect(url_for('homepage'))
        elif session['access_level'] != 'doctor':
            return redirect(url_for('homepage'))
        else:
            tending_physician = cursor.execute("select tending_physician from patients where patient_id=?", (pid)).fetchone()[0]
            if session['username'] != tending_physician:
                flash("You are a doctor but unauthorized to view this patients information")
                return redirect(url_for('homepage'))

        patient = cursor.execute("select * from patients where patient_id=?", (pid)).fetchone()
        cursor.close()
        file_submit = FileSubmit(request.form)
        file_submit.patient_nric.data=patient[1].strip()
        file_submit.patient_name.data=f"{patient[2].strip()} {patient[3].strip()}"


        if request.method == "POST" and file_submit.validate():
            if 'submission' not in request.files:
                flash("File has failed to be uploaded")
                return  redirect(url_for('submission'),pid)

            file = request.files["submission"]
            if file.filename.strip()=="":
                flash("Invalid filename","error")
                return  render_template('submission.html', form=file_submit,id=id)

            storedfiledata=get_file_data_from_database(pid)
            if  storedfiledata != None:
                if check_file_hash(storedfiledata[1],storedfiledata[2]):
                    print("Hash match")
                else:
                    print("Hash mismatch")
                    with open(os.path.join(app.config['UPLOAD_FOLDER'], storedfiledata[1]), "wb") as file_override:
                        file_override.write(storedfiledata[2])

            if allowed_filename(file.filename):
                path=os.path.join(app.config['UPLOAD_FOLDER'],'temp'+f"{patient[1].strip()}.docx")
                file.save(path)
                mainDocument=Document(os.path.join(app.config['UPLOAD_FOLDER'],f"{patient[1].strip()}.docx"))
                composer=Composer(mainDocument)
                toAddDocument=Document(path)
                composer.append(toAddDocument)
                composer.save(os.path.join(app.config['UPLOAD_FOLDER'],f"{patient[1].strip()}.docx"))
                os.remove(path)

                cursor = cnxn.cursor()
                alter_query = textwrap.dedent("UPDATE patient_file set file_content=?,file_last_modified_time=?,name_of_staff_that_modified_it=?,id_of_staff_modified_it=?,md5sum=? where patient_id=?;")
                filecontent = open(os.path.join(app.config['UPLOAD_FOLDER'], f"{patient[1].strip()}.docx"), "rb").read()
                md5Hash = hashlib.md5(filecontent)
                fileHashed = md5Hash.hexdigest()
                VALUES = (filecontent,datetime.now().today().strftime("%m/%d/%Y, %H:%M:%S"), "Staff_ID", 1, fileHashed,patient[0])
                cursor.execute(alter_query,VALUES)
                cursor.commit()
                cursor.close()

                flash("Patient record successfully updated")
                return redirect(url_for('homepage'))

            # md5Hash = hashlib.md5(readFile.encode("utf-8"))
            # md5Hashed = md5Hash.hexdigest()
            # transaction = blockchain.new_transaction(file_submit.recipient.data, file_submit.sender.data, md5Hashed)
            # blockchain.new_block('123')
            # return render_template('test.html', chain=blockchain.chain)
            return redirect(url_for("submission", pid=patient[0]))

        return render_template('submission.html', form=file_submit,id=pid)


    @app.route('/verification')
    @custom_login_required
    def verification():
        return render_template('verification.html')


    @app.route('/charts')
    @custom_login_required
    def charts():
        return render_template('charts.html')


    @app.route('/tables')
    @custom_login_required
    def tables():
        return render_template('table.html')


    @app.route('/export')
    #@custom_login_required
    def export():
        cursor = cnxn.cursor()
        cursor.execute("select patient_id,file_content from patient_file")
        results = cursor.fetchall()
        print(results)
        cursor.close()
        return render_template('export.html',results = results)


    @app.route('/data/<int:id>')
    #@custom_login_required
    def data(id):
        cursor = cnxn.cursor()
        cursor.execute("select file_content from patient_file where patient_id = ?",(id))
        data = cursor.fetchall()
        data = data[0][0].decode("utf-8")
        #print(data)
        mask = ''
        year = datetime.today().year
        # Age
        r = re.findall(r"(?i)(DOB.+)", data)
        date = re.findall(r"\d{4}", r[0])[0]
        age = year - int(date)
        age += random.randint(int(-age/10), int(age/10))
        mask += f'Age: {age}\n'
        # BMI
        r = re.findall(r"(?i)(?<=height:).?\d+.?\d+", data)[0].strip()
        if "." not in r:
            r = float(r) / 100
        height = float(r)
        r = re.findall(r"(?i)(?<=weight:).?\d+.?\d+", data)[0].strip()
        weight = float(r)
        bmi = weight / (height ** 2)
        bmi += random.randint(int(-bmi / 10), int(bmi / 10)) + random.uniform(-1, 1)
        mask += f'BMI: {bmi}\n'
        # Gender
        r = re.findall(r"(?i)(gender.+)", data)
        mask += f'{r[0]}\n'
        # Amount of times they visited
        r = re.findall(r"(?i)(medical history.+\n)((?:.+\n?)+){0,}", data)[0][1].split("\n")
        z = 0
        for i in range(len(r)):
            if str(year) in r[i]:
                z += 1
        z = z + random.randint(int(-z / 2), int(z / 2))
        mask += f'Visited Angel Health {z} times this year\n'
        r = re.findall(r"(?i)(diabetes)|(cancer)|(hiv)|(aids)", data)
        mask += f'Outstanding health problems:\n'
        if len(r) != 0:
            for i in r[0]:
                if i != '':
                    mask += f'{i.capitalize()}\n'
        else:
            mask += f'None'
        cursor.close()
        print(mask)
        return render_template('data.html',data = mask)

    @app.route('/appointment',methods=['GET','POST'])
    def appointment():
        appointment = Appointment(request.form)
        if request.method == "POST":
            if appointment.date.data <= date.today():
                print("date error")
                flash('Invalid date choice!','error')
                return redirect(url_for('appointment'))
            cursor = cnxn.cursor()
            user_appointment = str(appointment.date.data) + ", " + appointment.time.data
            print(user_appointment)
            cursor.execute("update patients set appointment = ? where username = ?",(user_appointment,session['patients']))
            flash(f'Your appointment has been booked on: {user_appointment}','success')
            return redirect(url_for('appointment'))
        print(session['patients'])
        return render_template('appointment.html', form = appointment)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        register = Register(request.form)

        if request.method == "POST" and register.validate():
            print("hello")
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                DATABASE=' + database + ';\
                Trusted_Connection=yes;'
            )
            username = register.username.data
            firstname = register.firstname.data
            lastname = register.lastname.data
            address = register.address.data
            phone_no = register.phone_no.data
            postal_code = register.postal_code.data
            email = register.email.data
            print(username)

            md5Hash = hashlib.md5(register.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            otp_code = pyotp.random_base32()
            insert_query = textwrap.dedent('''
                INSERT INTO patients (username, first_name, last_name, pass_hash, otp_code,email,phone_no,address,postal_code,access_level) 
                VALUES (?, ?, ?, ?, ?, ?,?,?,?,?); 
            ''')
            values = (username, firstname, lastname, md5Hashed, otp_code, email,phone_no,address,postal_code,'patient')
            cursor = cnxn.cursor()
            cursor.execute('SELECT username, email FROM patients')
            for x in cursor:
                if x.username == username or x.email == email:
                    return render_template('exists.html')

            cursor.execute(insert_query, values)
            #addPatient to access_list table ?
            insert_query = textwrap.dedent('''
                            INSERT INTO access_list (username, pass_hash,access_level) 
                            VALUES (?, ?, ?); 
                        ''')
            values = (username, md5Hashed,'patient')
            cursor.execute(insert_query,values)
            cnxn.commit()
            cursor.close()
            qr = 'otpauth://totp/AngelHealth:' + username + '?secret=' + otp_code

            return render_template('displayotp.html', otp=otp_code, qrotp=qr)

        return render_template('register.html', form=register)


    @app.route('/doctor-registration', methods=['GET', 'POST'])
    def register_doctor():
        doc_form = RegisterDoctor(request.form)
        if request.method == "POST" and doc_form.validate():
            cursor = cnxn.cursor()
            username = doc_form.username.data
            firstname = doc_form.firstname.data
            lastname = doc_form.lastname.data
            address = doc_form.address.data
            phone_no = doc_form.phone_no.data
            postal_code = doc_form.postal_code.data
            email = doc_form.email.data
            department = doc_form.department.data
            otp_code = pyotp.random_base32()
            md5Hash = hashlib.md5(doc_form.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            tables=["patients", "researchers", "hr", "head_admin", "doctors"]
            check = True
            for table in tables:
                check_username = cursor.execute("SELECT username FROM "+table+" WHERE username = ?",
                                                (username)).fetchval()  # prevent sql injection
                check_email = cursor.execute("SELECT email FROM "+table+" WHERE email = ?",
                                             (email)).fetchval()  # prevent sql injection
                if check_email == None and check_username == None:
                    continue
                else:
                    check = False
                    break

            if check:
                insert_query = "INSERT INTO doctors (username, first_name, last_name, pass_hash,email,otp_code,phone_no,access_level,postal_code,address,department) \
                                            VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?); "
                values = (username, firstname, lastname, md5Hashed,
                          email, otp_code, phone_no, 'doctor', address, postal_code, department)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                cursor = cnxn.cursor()
                insert_query = "INSERT INTO access_list (username,access_level,pass_hash) \
                                            VALUES (?, ?,?); "
                values = (username, 'doctor', md5Hashed)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                print('Sending email OTP...')
                qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                image = pyqrcode.create(qr)
                image.png('image.png', scale=5)
                SendMail("image.png", email, "Doctor")
                os.remove('image.png')
            return render_template('dashboard.html')
        return render_template('register_doctor.html', form=doc_form)

    @app.route('/patient-registration', methods=['GET', 'POST'])
    def register_patient():
        pat_form = Register(request.form)
        if request.method == "POST" and pat_form.validate():
            print("hello")
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=' + server + '; \
                DATABASE=' + database + ';\
                Trusted_Connection=yes;'
            )
            username = pat_form.username.data
            firstname = pat_form.firstname.data
            lastname = pat_form.lastname.data
            address = pat_form.address.data
            phone_no = pat_form.phone_no.data
            postal_code = pat_form.postal_code.data
            email = pat_form.email.data
            print(username)

            md5Hash = hashlib.md5(pat_form.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            otp_code = pyotp.random_base32()
            insert_query = textwrap.dedent('''
                INSERT INTO patients (username, first_name, last_name, pass_hash, otp_code,email,phone_no,address,postal_code,access_level) 
                VALUES (?, ?, ?, ?, ?, ?,?,?,?,?); 
            ''')
            values = (
            username, firstname, lastname, md5Hashed, otp_code, email, phone_no, address, postal_code, 'patient')

            cursor = cnxn.cursor()
            cursor.execute('SELECT username, email FROM patients')
            for x in cursor:
                if x.username == username or x.email == email:
                    return redirect(url_for('dashboard'))
            cursor.execute(insert_query, values)
            cnxn.commit()
            cursor.close()
            print('Sending email OTP...')
            qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
            image = pyqrcode.create(qr)
            image.png('image.png', scale=5)
            SendMail("image.png", email, "Researcher")
            os.remove('image.png')
            return redirect(url_for('dashboard'))
        return render_template('register_patient.html', form=pat_form)


    @app.route('/researchers-registration', methods=['GET', 'POST'])
    def register_researcher():
        researcher_form = RegisterResearcher(request.form)
        if request.method == "POST" and researcher_form.validate():
            cursor = cnxn.cursor()
            username = researcher_form.username.data
            firstname = researcher_form.firstname.data
            lastname = researcher_form.lastname.data
            address = researcher_form.address.data
            phone_no = researcher_form.phone_no.data
            postal_code = researcher_form.postal_code.data
            email = researcher_form.email.data
            company = researcher_form.company.data
            otp_code = pyotp.random_base32()
            md5Hash = hashlib.md5(researcher_form.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            tables = ["patients", "researchers", "hr", "head_admin", "doctors"]
            check = True
            for table in tables:
                check_username = cursor.execute("SELECT username FROM "+table+" WHERE username = ?",
                                                (username)).fetchval()  # prevent sql injection
                check_email = cursor.execute("SELECT email FROM "+table+" WHERE email = ?",
                                             (email)).fetchval()  # prevent sql injection
                if check_email == None and check_username == None:
                    continue
                else:
                    check = False
                    break

            if check:
                insert_query = "INSERT INTO researchers (username, first_name, last_name, pass_hash,email,otp_code,phone_no,access_level,postal_code,address,company) \
                                            VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?); "
                values = (username, firstname, lastname, md5Hashed,
                          email, otp_code, phone_no, 'researcher', address, postal_code, company)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                cursor = cnxn.cursor()
                insert_query = "INSERT INTO access_list (username,access_level,pass_hash) \
                                            VALUES (?, ?,?); "
                values = (username, 'researcher', md5Hashed)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                print('Sending email OTP...')
                qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                image = pyqrcode.create(qr)
                image.png('image.png', scale=5)
                SendMail("image.png", email, "Researcher")
                os.remove('image.png')
            return redirect(url_for('dashboard'))
        return render_template('register_researcher.html', form=researcher_form)


    @app.route('/hr-registration', methods=['GET', 'POST'])
    def register_hr():
        hr_form = RegisterHr(request.form)
        if request.method == "POST" and hr_form.validate():
            cursor = cnxn.cursor()
            username = hr_form.username.data
            firstname = hr_form.firstname.data
            lastname = hr_form.lastname.data
            address = hr_form.address.data
            phone_no = hr_form.phone_no.data
            postal_code = hr_form.postal_code.data
            email = hr_form.email.data
            otp_code = pyotp.random_base32()
            md5Hash = hashlib.md5(hr_form.password.data.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            tables = ["patients", "researchers", "hr", "head_admin", "doctors"]
            check = True
            for table in tables:
                check_username = cursor.execute("SELECT username FROM "+table+" WHERE username = ?",
                                                ( username)).fetchval()  # prevent sql injection
                check_email = cursor.execute("SELECT email FROM "+table+" WHERE email = ?",
                                             ( email)).fetchval()  # prevent sql injection
                if check_email == None and check_username == None:
                    continue
                else:
                    check = False
                    break

            if check:
                insert_query = "INSERT INTO hr (username, first_name, last_name, pass_hash,email,otp_code,phone_no,access_level,postal_code,address) \
                                                VALUES (?, ?, ?, ?, ?, ?,?,?,?,?); "
                values = (username, firstname, lastname, md5Hashed,
                          email, otp_code, phone_no, 'hr', postal_code,address)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                cursor = cnxn.cursor()
                insert_query = "INSERT INTO access_list (username,access_level,pass_hash) \
                                                VALUES (?, ?,?); "
                values = (username, 'hr', md5Hashed)
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                print('Sending email OTP...')
                qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                image = pyqrcode.create(qr)
                image.png('image.png', scale=5)
                SendMail("image.png", email, "Researcher")
                os.remove('image.png')
            return redirect(url_for('dashboard'))
        return render_template('register_hr.html', form=hr_form)

    @app.route('/<variable>/remove', methods=['GET', 'POST'])
    def remove(variable):
        return redirect(url_for('homepage'))

    @app.route('/<variable>/patient', methods=['GET', 'POST'])
    def patient(variable):
        return redirect(url_for('homepage'))

    @app.route('/<variable>/doctor', methods=['GET', 'POST'])
    def doctor(variable):
        return redirect(url_for('homepage'))

    @app.route('/<variable>/admin', methods=['GET', 'POST'])
    def admin(variable):
        return redirect(url_for('homepage'))

if __name__ == "__main__":
    add_admin()
    app.run(debug=True)
