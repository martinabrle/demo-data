
-- IF NOT EXISTS (SELECT * FROM sys.schemas where [name] = 'BikeSalesStaging')
--     CREATE SCHEMA BikeSalesStaging
-- GO

IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE [name] = 'SynapseDelimitedTextFormatSkipHeader') 
	CREATE EXTERNAL FILE FORMAT [SynapseDelimitedTextFormatSkipHeader] 
	WITH ( FORMAT_TYPE = DELIMITEDTEXT ,
	       FORMAT_OPTIONS (
			 FIELD_TERMINATOR = ',',
			 USE_TYPE_DEFAULT = TRUE,
             First_Row = 2
			))
GO

--DROP EXTERNAL DATA SOURCE [samples_data_lake] 
IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE [name] = 'samples_data_lake') 
	CREATE EXTERNAL DATA SOURCE [samples_data_lake] 
	WITH (
		LOCATION = 'abfss://samples@mabrledatasets.dfs.core.windows.net/' 
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Addresses')
    DROP EXTERNAL TABLE BikeSalesStaging.Addresses
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Customers')
    DROP EXTERNAL TABLE BikeSalesStaging.Customers
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Vendors')
    DROP EXTERNAL TABLE BikeSalesStaging.Vendors
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Employees')
    DROP EXTERNAL TABLE BikeSalesStaging.Employees
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductCategories')
    DROP EXTERNAL TABLE BikeSalesStaging.ProductCategories
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductCategoryTexts')
    DROP EXTERNAL TABLE BikeSalesStaging.ProductCategoryText
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Products')
    DROP EXTERNAL TABLE BikeSalesStaging.Products
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductTexts')
    DROP EXTERNAL TABLE BikeSalesStaging.ProductTexts
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'SalesOrderItems')
    DROP EXTERNAL TABLE BikeSalesStaging.SalesOrderItems
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'SalesOrders')
    DROP EXTERNAL TABLE BikeSalesStaging.SalesOrders
GO

CREATE EXTERNAL TABLE BikeSalesStaging.Addresses (
	[ADDRESSID] bigint,
	[CITY] nvarchar(80),
	[POSTALCODE] nvarchar(10),
	[STREET] nvarchar(80),
	[BUILDING] bigint,
	[COUNTRY] nvarchar(256),
	[REGION] nvarchar(256),
	[ADDRESSTYPE] bigint,
	[VALIDITY_STARTDATE] bigint,
	[VALIDITY_ENDDATE] bigint,
	[LATITUDE] float,
	[LONGITUDE] float
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/Addresses.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.Customers (
	[CUSTOMERID] bigint,
	[EMAILADDRESS] nvarchar(1024),
	[PHONENUMBER] nvarchar(20),
	[FAXNUMBER] nvarchar(20),
	[WEBADDRESS] nvarchar(1024),
	[ADDRESSID] bigint,
	[COMPANYNAME] nvarchar(256),
	[LEGALFORM] nvarchar(1024),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[CURRENCY] nvarchar(3)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/Customers.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.Vendors (
	[VENDORID] bigint,
	[EMAILADDRESS] nvarchar(1024),
	[PHONENUMBER] nvarchar(20),
	[FAXNUMBER] nvarchar(20),
	[WEBADDRESS] nvarchar(1024),
	[ADDRESSID] bigint,
	[COMPANYNAME] nvarchar(256),
	[LEGALFORM] nvarchar(1024),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[CURRENCY] nvarchar(3)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/Vendors.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.Employees (
	[EMPLOYEEID] bigint,
	[NAME_FIRST] nvarchar(80),
	[NAME_MIDDLE] nvarchar(80),
	[NAME_LAST] nvarchar(80),
	[NAME_INITIALS] nvarchar(10),
	[SEX] nvarchar(10),
	[LANGUAGE] nvarchar(5),
	[PHONENUMBER] nvarchar(20),
	[EMAILADDRESS] nvarchar(1024),
	[LOGINNAME] nvarchar(80),
	[ADDRESSID] bigint,
	[VALIDITY_STARTDATE] bigint,
	[VALIDITY_ENDDATE] bigint
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/Employees.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.ProductCategories (
	[PRODCATEGORYID] nvarchar(2),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/ProductCategories.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.ProductCategoryTexts (
	[PRODCATEGORYID] nvarchar(2),
	[LANGUAGE] nvarchar(5),
	[SHORT_DESCR] nvarchar(256),
	[MEDIUM_DESCR] nvarchar(1024),
	[LONG_DESCR] nvarchar(4000)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/ProductCategoryTexts.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.Products (
	[PRODUCTID] nvarchar(10),
	[TYPECODE] nvarchar(2),
	[PRODCATEGORYID] nvarchar(2),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[VENDORID] bigint,
	[TAXTARIFFCODE] bigint,
	[QUANTITYUNIT] nvarchar(10),
	[WEIGHTMEASURE] decimal(10,4),
	[WEIGHTUNIT] nvarchar(10),
	[CURRENCY] nvarchar(3),
	[PRICE] decimal(10,2),
	[WIDTH]decimal(10,4),
	[DEPTH] decimal(10,4),
	[HEIGHT] decimal(10,4),
	[DIMENSIONUNIT] nvarchar(80),
	[PRODUCTPICURL] nvarchar(1024)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/Products.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.ProductTexts (
	[PRODUCTID] nvarchar(10),
	[LANGUAGE] nvarchar(5),
	[SHORT_DESCR] nvarchar(256),
	[MEDIUM_DESCR] nvarchar(1024),
	[LONG_DESCR] nvarchar(4000)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/ProductTexts.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.SalesOrderItems (
	[SALESORDERID] bigint,
	[SALESORDERITEM] bigint,
	[PRODUCTID] nvarchar(10),
	[NOTEID] nvarchar(10),
	[CURRENCY] nvarchar(3),
	[GROSSAMOUNT] decimal(10,4),
	[NETAMOUNT] decimal(10,4),
	[TAXAMOUNT] decimal(10,4),
	[ITEMATPSTATUS] nvarchar(10),
	[OPITEMPOS] nvarchar(10),
	[QUANTITY] bigint,
	[QUANTITYUNIT] nvarchar(10),
	[DELIVERYDATE] bigint
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/SalesOrderItems.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE BikeSalesStaging.SalesOrders (
	[SALESORDERID] bigint,
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[FISCVARIANT] nvarchar(10),
	[FISCALYEARPERIOD] bigint,
	[NOTEID] nvarchar(10),
	[CUSTOMERID] bigint,
	[SALESORG] nvarchar(10),
	[CURRENCY] nvarchar(3),
	[GROSSAMOUNT] decimal(10,4),
	[NETAMOUNT] decimal(10,4),
	[TAXAMOUNT] decimal(10,4),
	[LIFECYCLESTATUS] nvarchar(10),
	[BILLINGSTATUS] nvarchar(10),
	[DELIVERYSTATUS] nvarchar(10)
	)
	WITH (
	LOCATION = 'Sample_Bike_Sales/SalesOrders.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

SELECT TOP 5 * FROM BikeSalesStaging.Addresses;
GO
SELECT TOP 5 * FROM BikeSalesStaging.Customers;
GO
SELECT TOP 5 * FROM BikeSalesStaging.Vendors;
GO
SELECT TOP 5 * FROM BikeSalesStaging.Employees;
GO
SELECT TOP 5 * FROM BikeSalesStaging.ProductCategories;
GO
SELECT TOP 5 * FROM BikeSalesStaging.ProductCategoryTexts;
GO
SELECT TOP 5 * FROM BikeSalesStaging.Products;
GO
SELECT TOP 5 * FROM BikeSalesStaging.ProductTexts;
GO
SELECT TOP 5 * FROM BikeSalesStaging.SalesOrderItems;
GO
SELECT TOP 5 * FROM BikeSalesStaging.SalesOrders;
GO
