CREATE TABLE [dbo].[SalesOrderItems] (

	[SALESORDERID] int NOT NULL, 
	[SALESORDERITEM] int NOT NULL, 
	[PRODUCTID] varchar(10) NOT NULL, 
	[NOTEID] varchar(10) NULL, 
	[CURRENCY] varchar(3) NULL, 
	[GROSSAMOUNT] decimal(10,4) NULL, 
	[NETAMOUNT] decimal(10,4) NULL, 
	[TAXAMOUNT] decimal(10,4) NULL, 
	[ITEMATPSTATUS] varchar(10) NULL, 
	[OPITEMPOS] varchar(10) NULL, 
	[QUANTITY] int NULL, 
	[QUANTITYUNIT] varchar(10) NULL, 
	[DELIVERYDATE] date NULL
);