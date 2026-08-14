CREATE TABLE [dbo].[VendorAddresses] (

	[ADDRESSID] int NOT NULL, 
	[CITY] varchar(80) NULL, 
	[POSTALCODE] varchar(10) NULL, 
	[STREET] varchar(80) NULL, 
	[BUILDING] int NULL, 
	[COUNTRY] varchar(256) NULL, 
	[REGION] varchar(256) NULL, 
	[ADDRESSTYPE] int NULL, 
	[VALIDITY_STARTDATE] date NULL, 
	[VALIDITY_ENDDATE] date NULL, 
	[LATITUDE] float NULL, 
	[LONGITUDE] float NULL
);