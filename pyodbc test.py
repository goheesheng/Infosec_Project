import pyodbc
import textwrap
from mssql_auth import database ,server
# Define the Price Data.
user_logins = [
    ['johnlim', 'John', 'Lim', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d', '6HDZKEGUIHTZLF35LPKKOX56XYGHUF7E']
]

# define the server and the database

# Define the connection string
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
    SERVER=' + server + '; \
    DATABASE=' + database + ';\
    Trusted_Connection=yes;'
)

def convert_into_binary(filepath):
    with open(filepath,'rb') as file:
        binary = file.read()

    return binary

data = convert_into_binary('patient_data/patient1.txt')

print(data)
# Create the Cursor.
cursor = cnxn.cursor()
"""
# Loop through to insert each row.
for index, row in enumerate(user_logins):
    # define an insert query with place holders for the values.
    insert_query = textwrap.dedent('''
        INSERT INTO patients (username, first_name, last_name, pass_hash, otp_code,email,data) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''')

    # define the values
    values = (row[0], row[1], row[2], row[3], row[4],'john@gmail.com',data)

    # insert the data into the database
    cursor.execute(insert_query, values)

# commit the inserts.
cnxn.commit()
"""

# grab all the rows from the table
cursor.execute('SELECT * FROM patients')
for row in cursor:
    print(row.username)
    a = row.data
    print(a)
with open('patient_data/patient1.txt','wb') as file:
    file.write(a)


# close the cursor and connection
cursor.close()
cnxn.close()