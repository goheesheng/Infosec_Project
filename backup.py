from re import DEBUG
import pyodbc
import pyodbc
from datetime import datetime
import os

## BACKUP DB
server = 'GOHDESKTOP\SQLEXPRESS'
def generate_backup():
    database = 'database1'
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + server + '; \
        DATABASE=' + database + ';\
        Trusted_Connection=yes;' \
        , autocommit=True
    )

    backup = "BACKUP DATABASE [database1] TO DISK = N'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\database1.bak'"
    cursor = connection.cursor().execute(backup)
    while (cursor.nextset()):
        pass
    print('Backup successful')
    connection.close()
# generate_backup()

## RESTORE DB
#
def restore_backup(db_bak_name,filepath):
    cnct_str = pyodbc.connect( # need use master db because 
        'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + 'GOHDESKTOP\SQLEXPRESS01' + '; \
        DATABASE=' + 'master' + ';\
        Trusted_Connection=yes;' \
        ,autocommit=True)
    executelock = ("alter database database1 set offline with rollback immediate ")
    releaselock = ("alter database database1 set online")
    cur = cnct_str.cursor()

    statement = (
        """RESTORE DATABASE [%s] FROM  DISK = N'%s' WITH RECOVERY, MOVE 'database' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.SQLEXPRESS01\\MSSQL\DATA\\database.mdf',MOVE 'database_log' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.SQLEXPRESS01\\MSSQL\DATA\\database_log.ldf', REPLACE""" % (db_bak_name, filepath)) #  file name and db must be the same
    cur.execute(executelock)
    cur.execute(statement)
    while cur.nextset():
        pass
    cur.execute(releaselock)
    print("restore_backup completed successfully")
    
# restore_backup('database1','C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\database1.bak')