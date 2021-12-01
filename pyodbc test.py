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

# Create the Cursor.
cursor = cnxn.cursor()

# Loop through to insert each row.
for index, row in enumerate(user_logins):
    # define an insert query with place holders for the values.
    insert_query = textwrap.dedent('''
        INSERT INTO user_logins (username, first_name, last_name, pass_hash, otp_code,email) 
        VALUES (?, ?, ?, ?, ?, ?);
    ''')

    # define the values
    values = (row[0], row[1], row[2], row[3], row[4],)

    # insert the data into the database
    cursor.execute(insert_query, values)

# commit the inserts.
cnxn.commit()

# grab all the rows from the table
cursor.execute('SELECT * FROM user_logins')
for row in cursor:
    print(row.username)

# close the cursor and connection
cursor.close()
cnxn.close()