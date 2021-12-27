import pyodbc
import pyodbc
from datetime import datetime
import os

## BACKUP DB
server = 'GOHDESKTOP\SQLEXPRESS'

database = 'database1'
def backup_mssql():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + server + '; \
        DATABASE=' + database + ';\
        Trusted_Connection=yes;' \
        , autocommit=True
    )

    backup = "BACKUP DATABASE [database1] TO DISK = N'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\database1.bak'"
    cursor = connection.cursor().execute(backup)
    print(cursor)
    connection.close()

## RESTORE DB
#


def restore_backup(db_bak_name,filepath):

    cnct_str = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + server + '; \
        DATABASE=' + 'backup' + ';\
        Trusted_Connection=yes;' \
        ,autocommit=True)

    cur = cnct_str.cursor()

    cur.execute(
        """RESTORE DATABASE [%s] FROM  DISK = N'%s' WITH  FILE = 1, NOUNLOAD, REPLACE, STATS = 5""" % (db_bak_name, filepath)) #  file name and db must be the same
    while cur.nextset():
        pass
    
    print("restore_backup completed successfully")
restore_backup('database1','C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\database1.bak')