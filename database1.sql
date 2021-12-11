USE [master]
GO
/****** Object:  Database [database1]    Script Date: 12/11/2021 8:46:31 AM ******/
CREATE DATABASE [database1]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'database', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\database.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'database_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\database_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [database1] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [database1].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [database1] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [database1] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [database1] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [database1] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [database1] SET ARITHABORT OFF 
GO
ALTER DATABASE [database1] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [database1] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [database1] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [database1] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [database1] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [database1] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [database1] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [database1] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [database1] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [database1] SET  DISABLE_BROKER 
GO
ALTER DATABASE [database1] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [database1] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [database1] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [database1] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [database1] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [database1] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [database1] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [database1] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [database1] SET  MULTI_USER 
GO
ALTER DATABASE [database1] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [database1] SET DB_CHAINING OFF 
GO
ALTER DATABASE [database1] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [database1] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [database1] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [database1] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [database1] SET QUERY_STORE = OFF
GO
USE [database1]
GO
/****** Object:  Table [dbo].[doctors]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[doctors](
	[staff_id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nchar](30) NOT NULL,
	[first_name] [nchar](30) NOT NULL,
	[last_name] [nchar](30) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,
	[otp_code] [varchar](50) NOT NULL,
	[email] [varchar](50) NOT NULL,
	[address] [varchar](50) NOT NULL,
	[postal_code] [varchar](6) NOT NULL,
	[department] [varchar](50) NOT NULL,
	[access_level][varchar](30) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[head_admin]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[head_admin](
	[head_admin_id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nchar](30) NOT NULL,
	[first_name] [nchar](30) NOT NULL,
	[last_name] [nchar](30) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,
	[otp_code] [varchar](50) NOT NULL,
	[email] [varchar](50) NOT NULL,
	[phone_no] [varchar](20) NOT NULL,
	[access_level][varchar](30) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[access_list]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[access_list](
	[username][nchar](30) NOT NULL,
	[access_level][varchar](30) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,

) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[hr]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[hr](
	[hr_id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nchar](10) NOT NULL,
	[first_name] [nchar](20) NOT NULL,
	[last_name] [nchar](20) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,
	[otp_code] [varchar](50) NOT NULL,
	[address] [varchar](50) NOT NULL,
	[postal_code] [varchar](6) NOT NULL,
	[email] [varchar](50) NOT NULL,
	[phone_no] [varchar](20) NOT NULL,
	[access_level][varchar](30) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[patient_file]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[patient_file](
	[patient_id] [int] IDENTITY(1,1) NOT NULL,
	[file_name] [varchar](20) NOT NULL,
	[file_content] [varbinary](max) NOT NULL,
	[file_last_modified_time] [varchar](20) NOT NULL,
	[name_of_staff_that_modified_it] [varchar](20) NOT NULL,
	[id_of_staff_modified_it] [int] NOT NULL,
	[md5sum_] [varchar](64) NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[patients]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[patients](
	[patient_id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nchar](30) NOT NULL,
	[first_name] [nchar](30) NOT NULL,
	[last_name] [nchar](30) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,
	[otp_code] [varchar](50) NOT NULL,
	[email] [varchar](50) NOT NULL,
	[phone_no] [varchar](20) NOT NULL,
	[address] [varchar](50) NOT NULL,
	[postal_code] [varchar](6) NOT NULL,
	[hospital] [varchar](50) NULL,
	[tending_physician] [varchar](50) NULL,
	[appointment] [varchar](20) NULL,
	[access_level][varchar](30) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[researchers]    Script Date: 12/11/2021 8:46:32 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[researchers](
	[username] [nchar](30) NOT NULL,
	[first_name] [nchar](30) NOT NULL,
	[last_name] [nchar](30) NOT NULL,
	[pass_hash] [varchar](50) NOT NULL,
	[otp_code] [varchar](50) NOT NULL,
	[email] [varchar](50) NOT NULL,
	[phone_no] [varchar](20) NOT NULL,
	[address] [varchar](50) NOT NULL,
	[postal_code] [varchar](6) NOT NULL,
	[company] [varchar](50) NULL,
	[researcher_id] [int] IDENTITY(1,1) NOT NULL,
	[access_level][varchar](30) NOT NULL
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [database1] SET  READ_WRITE 
GO
