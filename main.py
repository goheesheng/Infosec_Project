import hashlib
import ssl
import pyqrcode
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask import Flask, request, render_template, g, redirect, url_for, flash, session,send_from_directory
from werkzeug.utils import secure_filename
import pyotp
import os
import smtplib
import hashlib
import re
import bcrypt
from forms import FileSubmit, Patient_Login_form, Admin_Login_form,Otp, Register, RequestPatientInfo_Form
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
        print(session['login'],'wrapper')
        if session is None:
            return redirect(url_for('login'))
# fix this later ES
        if 'expirydate' not in app.config and app.config['expirydate']<= datetime.utcnow():
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

     
        print(session['login'],'wrapper222222')

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
    expression=re.compile(r"(?i)^[\w]*(.pdf)$")
    return re.fullmatch(expression,filename)

@app.route('/')
def main():
    return render_template('home.html')

with app.app_context():
    @app.route('/homepage')
    @custom_login_required
    def homepage():
        print("I AM AT")
        return render_template('homepage.html')


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
        msg['From'] = 'e@mail.cc'
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
            md5Hash = hashlib.md5(password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()
            cursor = cnxn.cursor()
            user_id = cursor.execute(
                "select patient_id from patients where username = ? and pass_hash = ?",
                (username, md5Hashed)).fetchval()  # prevent sql injection
            if user_id:
                session['patients'] = user_id
                cursor.close()
                cnxn.close()
                return redirect(url_for("otpvalidation"))
            else:
                cursor.close()
                cnxn.close()
                return render_template("404.html")
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
            researcherCheck = cursor.execute("select username from researchers where username = ? and pass_hash = ?",
                                             (username, md5Hashed)).fetchone()
            adminCheck = cursor.execute("select hr_id from hr where username = ? and pass_hash = ?",
                                        (username, md5Hashed)).fetchone()
            headadminCheck = cursor.execute("select username from head_admin where username = ? and pass_hash = ?",
                                            (username, md5Hashed)).fetchone()
            passed = True
            if doctorCheck != None:
                user_type = "doctors"
                identifier = doctorCheck[0]
            elif adminCheck != None:
                user_type = "admin"
                identifier = adminCheck[0]
            elif researcherCheck != None:
                user_type = "researchers"
                identifier = researcherCheck[0]
            elif headadminCheck != None:
                user_type = "head_admin"
                identifier = headadminCheck[0]
            else:
                passed = False
                return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)
            if passed:
                session['id'] = identifier.strip() #need strip to remove the spaces
                cursor.close()
                cnxn.close()
                session['otp-semi-login'] = True
                return redirect(url_for("otpvalidation")),session['id']
            else:
                cursor.close()
                cnxn.close()
                return render_template("404.html")
        else:
            return render_template("login.html", patient_login_form=patient_login_form, admin_login_form = admin_login_form)


    @app.route('/validation')
    @custom_login_required
    def otpvalidation():
        if session['otp-semi-login'] == True:
            print('true')
            print(session['id'],"id")
            session['login'] = True
            # session['head_admin']
            # session['patient_id'] = None
            # session['researcher_id'] = None
            # session['doctor_id'] = None
            # session['admin_id'] = None
            # session['head_admin_id'] = None
            # session['otp-semi-login'] = None # used to prevent attacker direct traversal to /validation url
            return redirect(url_for('homepage')), session['login']
        else:
            print('false')

            flash('Wrong username or password!')
            return render_template("login.html")


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
        return render_template('login.html')


    @app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
    def download(filename):
        #dpvalidationhere
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename)

    @app.route('/requestPatientInformation',methods=['GET','POST'])
    def requestPatientInformation():
        requestPatientInformationForm=RequestPatientInfo_Form(request.form)
        if request.method=='POST' and requestPatientInformationForm.validate():
            physician='tom'
            patient_id=2
            cursor = cnxn.cursor()
            retrived = cursor.execute("select tending_physician from patients where tending_physician=? and patient_id=?",(physician,patient_id)).fetchval()
            cnxn.commit()
            cursor.close()
            if retrived is None:
                copyfile(os.path.join(app.config['UPLOAD_FOLDER'],'basetemplate.docx'),os.path.join(app.config['UPLOAD_FOLDER'],f"{patient_id}.docx") )
                #write code to insert the file into db

            return redirect(url_for("submission",id=patient_id))
        return render_template("requestPatientInformation.html",form=requestPatientInformationForm)

    @app.route('/submission/<id>', methods=['GET', 'POST'])
    @custom_login_required
    def submission(id):
        file_submit = FileSubmit(request.form)

        if request.method == "POST" and file_submit.validate():
            if 'submission' not in request.files:
                flash("File has failed to be uploaded")
                return redirect(url_for('submission'))

            file = request.files["submission"]
            filename=file.filename
            if file.filename.strip()=="":
                flash("Invalid filename")
                return redirect(url_for('submission'))
            if allowed_filename(file.filename):
                filename=secure_filename(file.filename)
                path=os.path.join(app.config['UPLOAD FOLDER'],filename)
                file.save(path)
                with open(path,'rb') as savedFile:
                    savedFileBinaryData=savedFile.read()

                cursor = cnxn.cursor()
                insert_query = textwrap.dedent('''INSERT INTO PATIENTFILE (patient_id,file_name,file_content) VALUES (?, ?, ?); ''')
                VALUES=("123",filename,savedFileBinaryData)
                cursor.execute(insert_query,VALUES)
                cnxn.commit()
                cursor.close()

                return render_template('test.html')

            # md5Hash = hashlib.md5(readFile.encode("utf-8"))
            # md5Hashed = md5Hash.hexdigest()
            # transaction = blockchain.new_transaction(file_submit.recipient.data, file_submit.sender.data, md5Hashed)
            # blockchain.new_block('123')
            # return render_template('test.html', chain=blockchain.chain)
            return redirect(url_for('submission'))
        return render_template('submission.html', form=file_submit,id=id)


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
        cursor.execute("select * from patients") #fix this LZS
        results = cursor.fetchall()
        print(len(results),results,results[0].first_name,len(results[0].first_name))
        cursor.close()
        return render_template('export.html',results = results)


    @app.route('/data/<int:id>')
    #@custom_login_required
    def data(id):
        cursor = cnxn.cursor()
        cursor.execute("select data from patients where patient_id = ?",(id))
        data = cursor.fetchall()
        print(data)
        data = data[0].data.decode("utf-8")
        print(data)
        cursor.close()
        return render_template('data.html',data = data)


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
    add_admin()
    app.run(debug = True)
