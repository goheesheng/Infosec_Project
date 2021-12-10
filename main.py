import hashlib
import ssl
import pyqrcode
from docx import Document
from docxcompose.composer import Composer
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import *
from flask import Flask, request, render_template, g, redirect, url_for, flash, session,send_from_directory
import pyotp
import os
import smtplib
import hashlib
import re
import bcrypt
from forms import FileSubmit, Patient_Login_form, Admin_Login_form,Otp, Register, RequestPatientInfo_Form, Appointment
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
        users = cursor.execute("SELECT * FROM patients")
        print(users)
        return render_template('dashboard.html', patients=users)


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

    def SendMail(ImgFileName, email):
        with open(ImgFileName, 'rb') as f:
            img_data = f.read()
        sender = "IT2566proj@gmail.com"
        senderpass = 'FishNugget123'
        msg = MIMEMultipart()
        msg['Subject'] = 'Head Admin Qr Code For Google Authenticator'
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
                otp_code = pyotp.random_base32()

                md5Hash = hashlib.md5(admin_password.encode("utf-8"))
                md5Hashed = md5Hash.hexdigest()

                cursor = cnxn.cursor()
                check_username = cursor.execute("SELECT username FROM head_admin WHERE username = ?",
                                       (username)).fetchval()  # prevent sql injection
                check_email = cursor.execute("SELECT email FROM head_admin WHERE email = ?",
                                       (email)).fetchval()  # prevent sql injection

                if check_email == None and check_username == None :
                    insert_query = "INSERT INTO head_admin (username, first_name, last_name, pass_hash,email,otp_code) \
                            VALUES (?, ?, ?, ?, ?, ?); "
                    values = (username, firstname, lastname, md5Hashed,
                              email,
                              otp_code)  # i removed otp_code because this is server side config, how are we gonna add otp via terminal??, otp_code is last second column
                    cursor.execute(insert_query, values)
                    cursor.commit()
                    cursor.close()
                    print('Sending email OTP...')
                    qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                    image = pyqrcode.create(qr)
                    image.png('image.png', scale=5)
                    SendMail("image.png", email)
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
                        print(f"Username: {username}, First Name: {first_name}, Last Name: {last_name}, Email: {email}")
                    continue
                else:
                    print("Head Admin already exists! Check your username and email!!!!")
                # while str(a) == str(username):
                #     print("Head Admin already exist!")
                #     username = input("Enter New Head Admin ID again: ")
                #     check = cursor.execute("SELECT username FROM head_admin WHERE username = ?",(username)).fetchval()# prevent sql injection
                #     if check == None:
                #         firstname = input("Enter New Head Admin First Name: ")
                #         lastname = input("Enter New Head Admin last Name: ")
                #         email = input("Enter New Head Admin email: ")
                #         admin_password = input("Enter New Head Admin Password: ")
                #         md5Hash = hashlib.md5(admin_password.encode("utf-8"))
                #         md5Hashed = md5Hash.hexdigest()
                #         cursor = cnxn.cursor()
                #         insert_query = "INSERT INTO head_admin (username, first_name, last_name, pass_hash,email) \
                #             VALUES (?, ?, ?, ?, ?); "
                #         values = (username, firstname, lastname, md5Hashed, email) # i removed otp_code because this is server side config, how are we gonna add otp via terminal??, otp_code is last second column
                #         cursor.execute(insert_query, values)
                #         cursor.commit()
                #         cursor.close()
                #         print('Successful creating Head Admin')
                #         break
                #     else:
                #         a = check.strip()
                #         print(type(a))
                #         firstname = input("Enter New Head Admin First Name: ")
                #         lastname = input("Enter New Head Admin last Name: ")
                #         email = input("Enter New Head Admin email: ")
                #         admin_password = input("Enter New Head Admin Password: ")
                #         md5Hash = hashlib.md5(admin_password.encode("utf-8"))
                #         md5Hashed = md5Hash.hexdigest()
                #         print(a,'a')
                #         print(username,"b")
                #         continue
                # cursor = cnxn.cursor()
                # insert_query = "INSERT INTO head_admin (username, first_name, last_name, pass_hash,email) \
                #     VALUES (?, ?, ?, ?, ?); "
                # values = (username, firstname, lastname, md5Hashed, email) # i removed otp_code because this is server side config, how are we gonna add otp via terminal??, otp_code is last second column
                # cursor.execute(insert_query, values)
                # cursor.commit()
                # cursor.close()
                # print('Successful creating Head Admin')
                # continue


            # except:
            #     print("Error in adding Head Admin to MSSQL Database!")

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
            username = patient_login_form.username.data
            password = patient_login_form.password.data
            print(username,password)
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            print(md5Hashed)
            cursor = cnxn.cursor()
            user_id = cursor.execute(
                "select username, patient_id from patients where username = ? and pass_hash = ?",
                (username, md5Hashed)).fetchval()  # prevent sql injection
            if user_id:
                session['patients'] = user_id.strip()
                session['username'] = username.strip()
                cursor.close()
                cnxn.close()
                session['otp-semi-login'] = True
                print('user logged in')
                flash("Please continue with otp validation before login is successful","success")
                return redirect(url_for("otpvalidation"))
            else:
                cursor.close()
                cnxn.close()
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
            username = admin_login_form.username.data
            password = admin_login_form.password.data
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            cursor = cnxn.cursor()
            doctorCheck = cursor.execute("select staff_id from doctors where username = ? and pass_hash = ?",
                                         (username, md5Hashed)).fetchone()
            researcherCheck = cursor.execute("select researcher_id from researchers where username = ? and pass_hash = ?",
                                             (username, md5Hashed)).fetchone()
            adminCheck = cursor.execute("select hr_id from hr where username = ? and pass_hash = ?",
                                        (username, md5Hashed)).fetchone()
            headadminCheck = cursor.execute("select head_admin_id from head_admin where username = ? and pass_hash = ?",
                                            (username, md5Hashed)).fetchone()
            passed = True
            if doctorCheck != None:
                user_type = "doctors"
                identifier = doctorCheck[0]
                username = doctorCheck[1]

            elif adminCheck != None:
                user_type = "admin"
                identifier = adminCheck[0]
                username = doctorCheck[1]

            elif researcherCheck != None:
                user_type = "researchers"
                identifier = researcherCheck[0]
                username = doctorCheck[1]

            elif headadminCheck != None:
                user_type = "head_admin"
                identifier = headadminCheck[0]
                username = doctorCheck[1]

            else:
                passed = False
                return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)
            if passed:
                session['id'] = identifier.strip() #need strip to remove the spaces
                session['username'] = username.strip()
                cursor.close()
                cnxn.close()
                session['otp-semi-login'] = True
                return redirect(url_for("otpvalidation"))
            else:
                cursor.close()
                cnxn.close()
                return render_template("404.html")
        else:
            return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)


    @app.route('/validation2')
    # @custom_login_required
    def otpvalidation():
        if session['otp-semi-login'] == True:
            print('true')
            print(dict(session),'otp session check')
            # print(session['id'],"id")
            session['login'] = True
            # session['head_admin']
            # session['patient_id'] = None
            # session['researcher_id'] = None
            # session['doctor_id'] = None
            # session['admin_id'] = None
            # session['head_admin_id'] = None
            # session['otp-semi-login'] = None # used to prevent attacker direct traversal to /validation url
            flash("Login successful","success")
            return redirect(url_for('homepage')), session['login']
        else:
            print('false')
            flash('Wrong username or password!')
            return redirect(url_for("login"))


    @app.route("/validation", methods=["POST"])
    def otpvalidation2():
        cursor = cnxn.cursor()

        if "doctors" in session:
            (otp_seed, username, first_name, last_name) = cursor.execute(
                "select otp_code, username, first_name, last_name from doctors where staff_id = ?",
                (session["doctors"])
            ).fetchall()[0]
        elif "researchers" in session:
            (otp_seed, username, first_name, last_name) = cursor.execute(
                "select otp_code, username, first_name, last_name from researchers where researcher_id = ?",
                (session["researchers"])
            ).fetchall()[0]
        elif "patients" in session:
            (otp_seed, username, first_name, last_name) = cursor.execute(
                "select otp_code, username, first_name, last_name from patients where patient_id = ?",
                (session["patients"])
            ).fetchall()[0]
        elif "hr" in session:
            (otp_seed, username, first_name, last_name) = cursor.execute(
                "select otp_code, username, first_name, last_name from admin where username = ?",
                (session["admin"])
            ).fetchall()[0]
        elif "head_admin" in session:
            (otp_seed, username, first_name, last_name) = cursor.execute(
                "select otp_code, username, first_name, last_name from head_admin where username = ?",
                (session["head_admin"])
            ).fetchall()[0]

        # getting OTP provided by user
        otp = int(request.form.get("otp"))
        print(otp_seed)
        print(pyotp.TOTP(otp_seed).now())
        # verifying submitted OTP with PyOTP
        if pyotp.TOTP(otp_seed).verify(int(otp)):
            print("correct")
            string_otpseed = str(otp_seed)
            # info = cursor.execute(
            #     "select username, first_name, last_name, verification  from users where otp_code=\'" + str(
            #         otp_seed) + "\'").fetchall()
            session['username'] = username
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['login'] = True

            cursor.close()
            cnxn.close()
            '''
            if verification == 'unverified':
                return redirect(url_for("unverified"))
            elif verification == 'patient':
                return redirect(url_for('patient'))
            elif verification == 'doctor':
                return redirect(url_for('doctor'))
            elif verification == 'admin':
                return redirect(url_for('admin'))
            elif verification == 'head_admin':
                return redirect(url_for('head_admin'))
            elif verification == 'researcher':
                return redirect(url_for('researcher'))'''
            return redirect(url_for('homepage'))
        else:
            print("wrong")
            cursor.close()
            cnxn.close()
            return redirect(url_for("login"))


    @app.route('/passwordreset', methods=['GET', 'POST'])
    @custom_login_required
    def passwordreset():
        return render_template('passwordreset.html')


    @app.route('/logout', methods=['GET', 'POST'])
    @custom_login_required
    def logout():
        session.clear()
        return redirect(url_for("login"))


    @app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
    def download(filename):
        #dpvalidationhere
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
                    return redirect(url_for("submission", pid=patient[0]))

                cursor.close()
            flash("NRIC either does not exist or is invalid", "error")
            return redirect(url_for('requestPatientInformation'))
        return render_template("requestPatientInformation.html",form=requestPatientInformationForm)

    @app.route('/submission/<pid>', methods=['GET', 'POST'])
    # @login_required
    def submission(pid):
        cursor = cnxn.cursor()
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
        #print(len(results),results,results[0].first_name,len(results[0].first_name))
        cursor.close()
        return render_template('export.html',results = results)


    @app.route('/data/<int:id>')
    #@custom_login_required
    def data(id):
        cursor = cnxn.cursor()
        cursor.execute("select file_content from patient_file where patient_id = ?",(id))
        data = cursor.fetchall()
        data = data[0][0].decode("utf-8")
        print(data)
        cursor.close()
        return render_template('data.html',data = data)

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
            insert_query = textwrap.dedent('''
                INSERT INTO patients (username, first_name, last_name, pass_hash, otp_code,email) 
                VALUES (?, ?, ?, ?, ?, ?); 
            ''')
            values = (username, firstname, lastname, md5Hashed, otp_code, email)

            cursor = cnxn.cursor()
            cursor.execute('SELECT username, email FROM patients')
            for x in cursor:
                if x.username == username or x.email == email:
                    return render_template('exists.html')

            cursor.execute(insert_query, values)
            cnxn.commit()
            cursor.close()
            cnxn.close()
            qr = 'otpauth://totp/AngelHealth:' + username + '?secret=' + otp_code
            return render_template('displayotp.html', otp=otp_code, qrotp=qr)

        return render_template('register.html', form=register)


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
    #add_admin()
    app.run()
