--This script functions to remove all encryption keys, certificate that is created
--Turn off encrpytion
ALTER DATABASE database1
SET Encryption OFF
GO

--Remove database encrpytion key
use database1;
GO
DROP DATABASE ENCRYPTION KEY  ;
GO

--Remove certificate and master key
USE master;
GO
DROP CERTIFICATE ServerCert;
DROP MASTER KEY;
GO