CREATE TABLE [dbo].[Products] (

	[PRODUCTID] varchar(10) NOT NULL, 
	[TYPECODE] varchar(2) NULL, 
	[PRODCATEGORYID] varchar(2) NOT NULL, 
	[CREATEDBY] int NULL, 
	[CREATEDAT] date NULL, 
	[CHANGEDBY] int NULL, 
	[CHANGEDAT] date NULL, 
	[VENDORID] int NULL, 
	[TAXTARIFFCODE] int NULL, 
	[QUANTITYUNIT] varchar(10) NULL, 
	[WEIGHTMEASURE] decimal(10,4) NULL, 
	[WEIGHTUNIT] varchar(10) NULL, 
	[CURRENCY] varchar(3) NULL, 
	[PRICE] decimal(10,2) NULL, 
	[WIDTH] decimal(10,4) NULL, 
	[DEPTH] decimal(10,4) NULL, 
	[HEIGHT] decimal(10,4) NULL, 
	[DIMENSIONUNIT] varchar(80) NULL, 
	[PRODUCTPICURL] varchar(1024) NULL
);