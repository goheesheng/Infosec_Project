--REMEMBER TO PARSE IN THE PASSWORD GIVEN TO IMPORT CERTIFICATES AND CHECK PATH OF CERTIFICATES
--CREATE MASTER KEY on current instance (using ur own password for this db)
USE MASTER
GO
CREATE MASTER KEY ENCRYPTION BY PASSWORD ='masterPASSWORD'
GO

--Restore certificate with reference to earlier private key and decrypt it with same password. (using the shared password)
CREATE CERTIFICATE SERVERCERT
FROM FILE= 'C:\BACKUP\ServerCert.cer'
WITH PRIVATE KEY (FILE='C:\Backup\ServerCert_Cert_Key.pvk',DECRYPTION BY PASSWORD ='certPASSWORD')
GO

--Create Encryption Key, Encrypted by Server Certificate
USE database1;
GO
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE SERVERCERT;
GO


--Restore DB
USE master

RESTORE DATABASE [database1] FROM  DISK = N'C:\BACKUP\database1.bak' WITH RECOVERY, MOVE 'database' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.MSSQLSERVER01\\MSSQL\DATA\\database.mdf',MOVE 'database_log' TO 'C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\MSSQL15.MSSQLSERVER01\\MSSQL\DATA\\database_log.ldf', REPLACE

