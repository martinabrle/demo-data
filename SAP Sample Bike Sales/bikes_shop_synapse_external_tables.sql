
-- IF NOT EXISTS (SELECT * FROM sys.schemas where [name] = 'Bikes')
--     CREATE SCHEMA Bikes
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

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE [name] = 'bikes_shop_data_lake') 
	CREATE EXTERNAL DATA SOURCE [bikes_shop_data_lake] 
	WITH (
		LOCATION = 'abfss://[container_name]@[data_lake_name].dfs.core.windows.net' 
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Addresses')
    DROP EXTERNAL TABLE Bikes.Addresses
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'BusinessPartners')
    DROP EXTERNAL TABLE Bikes.BusinessPartners
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Employees')
    DROP EXTERNAL TABLE Bikes.Employees
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductCategories')
    DROP EXTERNAL TABLE Bikes.ProductCategories
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductCategoryText')
    DROP EXTERNAL TABLE Bikes.ProductCategoryText
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'Products')
    DROP EXTERNAL TABLE Bikes.Products
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProductTexts')
    DROP EXTERNAL TABLE Bikes.ProductTexts
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'SalesOrderItems')
    DROP EXTERNAL TABLE Bikes.SalesOrderItems
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'SalesOrders')
    DROP EXTERNAL TABLE Bikes.SalesOrders
GO


CREATE EXTERNAL TABLE Bikes.Addresses (
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
	LOCATION = 'bikes_shop/Addresses.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO


CREATE EXTERNAL TABLE Bikes.BusinessPartners (
	[PARTNERID] bigint,
	[PARTNERROLE] bigint,
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
	LOCATION = 'bikes_shop/BusinessPartners.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.Employees (
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
	LOCATION = 'bikes_shop/Employees.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.ProductCategories (
	[PRODCATEGORYID] nvarchar(2),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint
	)
	WITH (
	LOCATION = 'bikes_shop/ProductCategories.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.ProductCategoryText (
	[PRODCATEGORYID] nvarchar(2),
	[LANGUAGE] nvarchar(5),
	[SHORT_DESCR] nvarchar(256),
	[MEDIUM_DESCR] nvarchar(1024),
	[LONG_DESCR] nvarchar(4000)
	)
	WITH (
	LOCATION = 'bikes_shop/ProductCategoryText.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.Products (
	[PRODUCTID] nvarchar(10),
	[TYPECODE] nvarchar(2),
	[PRODCATEGORYID] nvarchar(2),
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[SUPPLIER_PARTNERID] bigint,
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
	LOCATION = 'bikes_shop/Products.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.ProductTexts (
	[PRODUCTID] nvarchar(10),
	[LANGUAGE] nvarchar(5),
	[SHORT_DESCR] nvarchar(256),
	[MEDIUM_DESCR] nvarchar(1024),
	[LONG_DESCR] nvarchar(4000)
	)
	WITH (
	LOCATION = 'bikes_shop/ProductTexts.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.SalesOrderItems (
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
	LOCATION = 'bikes_shop/SalesOrderItems.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

CREATE EXTERNAL TABLE Bikes.SalesOrders (
	[SALESORDERID] bigint,
	[CREATEDBY] bigint,
	[CREATEDAT] bigint,
	[CHANGEDBY] bigint,
	[CHANGEDAT] bigint,
	[FISCVARIANT] nvarchar(10),
	[FISCALYEARPERIOD] bigint,
	[NOTEID] nvarchar(10),
	[PARTNERID] bigint,
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
	LOCATION = 'bikes_shop/SalesOrders.csv',
	DATA_SOURCE = [bikes_shop_data_lake],
	FILE_FORMAT = [SynapseDelimitedTextFormatSkipHeader]
	)
GO

SELECT TOP 5 * FROM Bikes.Addresses;
GO
SELECT TOP 5 * FROM Bikes.BusinessPartners;
GO
SELECT TOP 5 * FROM Bikes.Employees;
GO
SELECT TOP 5 * FROM Bikes.ProductCategories;
GO
SELECT TOP 5 * FROM Bikes.ProductCategoryText;
GO
SELECT TOP 5 * FROM Bikes.Products;
GO
SELECT TOP 5 * FROM Bikes.ProductTexts;
GO
SELECT TOP 5 * FROM Bikes.SalesOrderItems;
GO
SELECT TOP 5 * FROM Bikes.SalesOrders;
GO
