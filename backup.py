from re import DEBUG
import pyodbc,time
from datetime import datetime
import os


#This file is used for testing purposes

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
    t = time.localtime()
    # current_time = str(time.strftime("%d %B %Y_(%H,%M,%S)",t))
    current_time = time.strftime("%m/%d/%Y, %H:%M:%S",t)

    backup = f"BACKUP DATABASE [database1] TO DISK = N'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\{current_time}.bak'"
    # backup = "BACKUP DATABASE [database1] TO DISK = N'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\database1.bak'"
    cursor = connection.cursor().execute(backup)
    while (cursor.nextset()):
        pass
    print('Backup successful')
    connection.close()
# generate_backup()

## RESTORE DB
#
def restore_backup():
    cnct_str = pyodbc.connect( # need use master db because 
        'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=' + 'GOHDESKTOP\SQLEXPRESS' + '; \
        DATABASE=' + 'database1' + ';\
        Trusted_Connection=yes;' \
        ,autocommit=True)
    executelock = ("alter database database1 set offline with rollback immediate ")
    releaselock = ("alter database database1 set online")
    cur = cnct_str.cursor()

    #restore to server 2
    # statement = (
    #     """RESTORE DATABASE [%s] FROM  DISK = N'%s' WITH RECOVERY, MOVE 'database' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.SQLEXPRESS01\\MSSQL\DATA\\database.mdf',MOVE 'database_log' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.SQLEXPRESS01\\MSSQL\DATA\\database_log.ldf', REPLACE""" % (db_bak_name, filepath)) #  file name and db must be the same
    #restore to server 1 btm 3 lines
    folder_path = "C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\"
    folders = os.listdir(folder_path) #['folder1', 'folder2'] list folder
    statement = f"RESTORE DATABASE database1 FROM  DISK = N'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\{folders[-1]}' WITH RECOVERY, MOVE 'database' TO 'C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL\\DATA\\database.mdf',MOVE 'database_log' TO 'C:\\Program Files\\Microsoft SQL Server\\MSSQL15.SQLEXPRESS\\MSSQL\\DATA\\database_log.ldf', REPLACE" #  file name and db must be the same
    
    cur.execute(executelock)
    cur.execute(statement)
    while cur.nextset():
        pass
    cur.execute(releaselock)
    print("restore_backup completed successfully")
    
restore_backup()