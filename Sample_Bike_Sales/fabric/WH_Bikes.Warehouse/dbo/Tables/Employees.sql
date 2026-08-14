CREATE TABLE [dbo].[Employees] (

	[EMPLOYEEID] int NOT NULL, 
	[NAME_FIRST] varchar(80) NULL, 
	[NAME_MIDDLE] varchar(80) NULL, 
	[NAME_LAST] varchar(80) NULL, 
	[NAME_INITIALS] varchar(10) NULL, 
	[SEX] varchar(10) NULL, 
	[LANGUAGE] varchar(5) NULL, 
	[PHONENUMBER] varchar(20) NULL, 
	[EMAILADDRESS] varchar(1024) NULL, 
	[LOGINNAME] varchar(80) NULL, 
	[ADDRESSID] int NULL, 
	[VALIDITY_STARTDATE] date NULL, 
	[VALIDITY_ENDDATE] date NULL
);