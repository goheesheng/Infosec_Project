from mssql_auth import server, database
import pyodbc
import hashlib
import pyotp
import smtplib
import pyqrcode
from email.mime.image import MIMEImage


def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # Not SSL
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.ehlo()
    # server.starttls()
    # server.login(user, pwd)
    # server.sendmail(FROM, TO, message)
    # server.close()
    # print ('successfully sent the mail')
    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("64.233.167.109", 465)
    server_ssl.ehlo()  # optional, called by login()
    server_ssl.login(user, pwd)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(FROM, TO, message)
    # server_ssl.quit()
    server_ssl.close()
    print('successfully sent the mail')


def add_admin():
    cnxn = pyodbc.connect(
     'DRIVER={ODBC Driver 17 for SQL Server}; \
     SERVER=' + server + '; \
     DATABASE=' + database + ';\
     Trusted_Connection=yes;'
    )
    while True:
        key = input("Do you want to create Head Admin ID and password? (Y/N/Show/Delete)").capitalize()
        if key == "Y":
            username = input("Enter New Head Admin ID: ")
            cursor = cnxn.cursor()
            check = cursor.execute("SELECT username FROM head_admin WHERE username = ?",
                                   (username)).fetchval()  # prevent sql injection

            firstname = input("Enter New Head Admin First Name: ")
            lastname = input("Enter New Head Admin last Name: ")
            email = input("Enter New Head Admin email: ")
            admin_password = input("Enter New Head Admin Password: ")
            otp_code = pyotp.random_base32(

            )

            md5Hash = hashlib.md5(admin_password.encode("utf-8"))
            md5Hashed = md5Hash.hexdigest()

            cursor = cnxn.cursor()
            check = cursor.execute("SELECT username FROM head_admin WHERE username = ?",
                                   (username)).fetchval()  # prevent sql injection
            if check == None:
                insert_query = "INSERT INTO head_admin (username, first_name, last_name, pass_hash,email,otp_code) \
                        VALUES (?, ?, ?, ?, ?, ?); "
                values = (username, firstname, lastname, md5Hashed,
                          email,otp_code)  # i removed otp_code because this is server side config, how are we gonna add otp via terminal??, otp_code is last second column
                cursor.execute(insert_query, values)
                cursor.commit()
                cursor.close()
                print('Successful creating Head Admin')
                qr = 'otpauth://totp/AngelHealth:' + str(username) + '?secret=' + otp_code
                image = MIMEImage
                send_email("appdevescip2003@gmail.com","appdev7181",email, "OTP CODE", "pyqrcode.create(qr)")
                print( "Successfully sent email")
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
                print("Head Admin already exists!")
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

add_admin()