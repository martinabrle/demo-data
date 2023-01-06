-- IF NOT EXISTS (SELECT * FROM sys.schemas where [name] = 'AdventureWorksDWStaging')
--     CREATE SCHEMA AdventureWorksDWStaging
-- GO

IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE [name] = 'SynapsePipeDelimitedTextFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapsePipeDelimitedTextFormat] 
	WITH ( FORMAT_TYPE = DELIMITEDTEXT ,
	       FORMAT_OPTIONS (
			 FIELD_TERMINATOR = '|',
			 USE_TYPE_DEFAULT = TRUE,
             First_Row = 1
			))
GO

IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE [name] = 'SynapseTabDelimitedTextFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseTabDelimitedTextFormat] 
	WITH ( FORMAT_TYPE = DELIMITEDTEXT ,
	       FORMAT_OPTIONS (
			 FIELD_TERMINATOR = '\t',
			 USE_TYPE_DEFAULT = TRUE,
             First_Row = 1
			))
GO

--DROP EXTERNAL DATA SOURCE [samples_data_lake] 
IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE [name] = 'samples_data_lake') 
	CREATE EXTERNAL DATA SOURCE [samples_data_lake] 
	WITH (
		LOCATION = 'abfss://[container]@[storage_acct].dfs.core.windows.net/' 
	)
GO

--DROP EXTERNAL TABLE [AdventureWorksDWStaging].[AdventureWorksDWBuildVersion]

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'AdventureWorksDWBuildVersion')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[AdventureWorksDWBuildVersion]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[AdventureWorksDWBuildVersion](
    [SystemInformationID] [tinyint],
	[DBVersion] [nvarchar](25),
	[VersionDate] datetime,
    [ModifiedDate] datetime
) WITH (
	LOCATION = 'AdventureWorks/AWBuildVersion.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapseTabDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimAccount')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimAccount]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimAccount](
	[AccountKey] [int],
	[ParentAccountKey] [int],
	[AccountCodeAlternateKey] [int],
	[ParentAccountCodeAlternateKey] [int],
	[AccountDescription] [nvarchar](50),
	[AccountType] [nvarchar](50),
	[Operator] [nvarchar](50),
	[CustomMembers] [nvarchar](300),
	[ValueType] [nvarchar](50),
	[CustomMemberOptions] [nvarchar](200) 
) WITH (
	LOCATION = 'AdventureWorksDW/DimAccount.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimCurrency')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimCurrency]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimCurrency](
	[CurrencyKey] [int],
	[CurrencyAlternateKey] [nchar](3),
	[CurrencyName] [nvarchar](50)
) WITH (
	LOCATION = 'AdventureWorksDW/DimCurrency.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimCustomer')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimCustomer]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimCustomer](
	[CustomerKey] [int],
	[GeographyKey] [int],
	[CustomerAlternateKey] [nvarchar](15),
	[Title] [nvarchar](8),
	[FirstName] [nvarchar](50),
	[MiddleName] [nvarchar](50),
	[LastName] [nvarchar](50),
	[NameStyle] [bit],
	[BirthDate] [date],
	[MaritalStatus] [nchar](1),
	[Suffix] [nvarchar](10),
	[Gender] [nvarchar](1),
	[EmailAddress] [nvarchar](50),
	[YearlyIncome] [money],
	[TotalChildren] [tinyint],
	[NumberChildrenAtHome] [tinyint],
	[EnglishEducation] [nvarchar](40),
	[SpanishEducation] [nvarchar](40),
	[FrenchEducation] [nvarchar](40),
	[EnglishOccupation] [nvarchar](100),
	[SpanishOccupation] [nvarchar](100),
	[FrenchOccupation] [nvarchar](100),
	[HouseOwnerFlag] [nchar](1),
	[NumberCarsOwned] [tinyint],
	[AddressLine1] [nvarchar](120),
	[AddressLine2] [nvarchar](120),
	[Phone] [nvarchar](20),
	[DateFirstPurchase] [date],
	[CommuteDistance] [nvarchar](15)
) WITH (
	LOCATION = 'AdventureWorksDW/DimCustomer.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimDate')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimDate]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimDate](
	[DateKey] [int],
	[FullDateAlternateKey] [date],
	[DayNumberOfWeek] [tinyint],
	[EnglishDayNameOfWeek] [nvarchar](10),
	[SpanishDayNameOfWeek] [nvarchar](10),
	[FrenchDayNameOfWeek] [nvarchar](10),
	[DayNumberOfMonth] [tinyint],
	[DayNumberOfYear] [smallint],
	[WeekNumberOfYear] [tinyint],
	[EnglishMonthName] [nvarchar](10),
	[SpanishMonthName] [nvarchar](10),
	[FrenchMonthName] [nvarchar](10),
	[MonthNumberOfYear] [tinyint],
	[CalendarQuarter] [tinyint],
	[CalendarYear] [smallint],
	[CalendarSemester] [tinyint],
	[FiscalQuarter] [tinyint],
	[FiscalYear] [smallint],
	[FiscalSemester] [tinyint]
) WITH (
	LOCATION = 'AdventureWorksDW/DimDate.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimDepartmentGroup')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimDepartmentGroup]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimDepartmentGroup](
	[DepartmentGroupKey] [int],
	[ParentDepartmentGroupKey] [int],
	[DepartmentGroupName] [nvarchar](50)
) WITH (
	LOCATION = 'AdventureWorksDW/DimDepartmentGroup.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimEmployee')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimEmployee]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimEmployee](
	[EmployeeKey] [int],
	[ParentEmployeeKey] [int],
	[EmployeeNationalIDAlternateKey] [nvarchar](15),
	[ParentEmployeeNationalIDAlternateKey] [nvarchar](15),
	[SalesTerritoryKey] [int],
	[FirstName] [nvarchar](50),
	[LastName] [nvarchar](50),
	[MiddleName] [nvarchar](50),
	[NameStyle] [bit],
	[Title] [nvarchar](50),
	[HireDate] [date],
	[BirthDate] [date],
	[LoginID] [nvarchar](256),
	[EmailAddress] [nvarchar](50),
	[Phone] [nvarchar](25),
	[MaritalStatus] [nchar](1),
	[EmergencyContactName] [nvarchar](50),
	[EmergencyContactPhone] [nvarchar](25),
	[SalariedFlag] [bit],
	[Gender] [nchar](1),
	[PayFrequency] [tinyint],
	[BaseRate] [money],
	[VacationHours] [smallint],
	[SickLeaveHours] [smallint],
	[CurrentFlag] [bit],
	[SalesPersonFlag] [bit],
	[DepartmentName] [nvarchar](50),
	[StartDate] [date],
	[EndDate] [date],
	[Status] [nvarchar](50),
	[EmployeePhoto] [varbinary](max)
) WITH (
	LOCATION = 'AdventureWorksDW/DimEmployee.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimGeography')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimGeography]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimGeography](
	[GeographyKey] [int],
	[City] [nvarchar](30),
	[StateProvinceCode] [nvarchar](3),
	[StateProvinceName] [nvarchar](50),
	[CountryRegionCode] [nvarchar](3),
	[EnglishCountryRegionName] [nvarchar](50),
	[SpanishCountryRegionName] [nvarchar](50),
	[FrenchCountryRegionName] [nvarchar](50),
	[PostalCode] [nvarchar](15),
	[SalesTerritoryKey] [int],
	[IpAddressLocator] [nvarchar](15)
) WITH (
	LOCATION = 'AdventureWorksDW/DimGeography.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimOrganization')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimOrganization]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimOrganization](
	[OrganizationKey] [int],
	[ParentOrganizationKey] [int],
	[PercentageOfOwnership] [nvarchar](16),
	[OrganizationName] [nvarchar](50),
	[CurrencyKey] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/DimOrganization.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimProduct')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimProduct]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimProduct](
	[ProductKey] [int],
	[ProductAlternateKey] [nvarchar](25),
	[ProductSubcategoryKey] [int],
	[WeightUnitMeasureCode] [nchar](3),
	[SizeUnitMeasureCode] [nchar](3),
	[EnglishProductName] [nvarchar](50),
	[SpanishProductName] [nvarchar](50),
	[FrenchProductName] [nvarchar](50),
	[StandardCost] [money],
	[FinishedGoodsFlag] [bit],
	[Color] [nvarchar](15),
	[SafetyStockLevel] [smallint],
	[ReorderPoint] [smallint],
	[ListPrice] [money],
	[Size] [nvarchar](50),
	[SizeRange] [nvarchar](50),
	[Weight] decimal(10,4),
	[DaysToManufacture] [int],
	[ProductLine] [nchar](2),
	[DealerPrice] [money],
	[Class] [nchar](2),
	[Style] [nchar](2),
	[ModelName] [nvarchar](50),
	[LargePhoto] [varbinary](max),
	[EnglishDescription] [nvarchar](400),
	[FrenchDescription] [nvarchar](400),
	[ChineseDescription] [nvarchar](400),
	[ArabicDescription] [nvarchar](400),
	[HebrewDescription] [nvarchar](400),
	[ThaiDescription] [nvarchar](400),
	[GermanDescription] [nvarchar](400),
	[JapaneseDescription] [nvarchar](400),
	[TurkishDescription] [nvarchar](400),
	[StartDate] [datetime],
	[EndDate] [datetime],
	[Status] [nvarchar](7)
) WITH (
	LOCATION = 'AdventureWorksDW/DimProduct.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimProductCategory')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimProductCategory]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimProductCategory](
	[ProductCategoryKey] [int],
	[ProductCategoryAlternateKey] [int],
	[EnglishProductCategoryName] [nvarchar](50),
	[SpanishProductCategoryName] [nvarchar](50),
	[FrenchProductCategoryName] [nvarchar](50)
) WITH (
	LOCATION = 'AdventureWorksDW/DimProductCategory.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimProductSubcategory')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimProductSubcategory]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimProductSubcategory](
	[ProductSubcategoryKey] [int],
	[ProductSubcategoryAlternateKey] [int],
	[EnglishProductSubcategoryName] [nvarchar](50),
	[SpanishProductSubcategoryName] [nvarchar](50),
	[FrenchProductSubcategoryName] [nvarchar](50),
	[ProductCategoryKey] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/DimProductSubcategory.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimPromotion')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimPromotion]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimPromotion](
	[PromotionKey] [int],
	[PromotionAlternateKey] [int],
	[EnglishPromotionName] [nvarchar](255),
	[SpanishPromotionName] [nvarchar](255),
	[FrenchPromotionName] [nvarchar](255),
	[DiscountPct] float,
	[EnglishPromotionType] [nvarchar](50),
	[SpanishPromotionType] [nvarchar](50),
	[FrenchPromotionType] [nvarchar](50),
	[EnglishPromotionCategory] [nvarchar](50),
	[SpanishPromotionCategory] [nvarchar](50),
	[FrenchPromotionCategory] [nvarchar](50),
	[StartDate] [datetime],
	[EndDate] [datetime],
	[MinQty] [int],
	[MaxQty] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/DimPromotion.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimReseller')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimReseller]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimReseller](
	[ResellerKey] [int],
	[GeographyKey] [int],
	[ResellerAlternateKey] [nvarchar](15),
	[Phone] [nvarchar](25),
	[BusinessType] [varchar](20),
	[ResellerName] [nvarchar](50),
	[NumberEmployees] [int],
	[OrderFrequency] [char](1),
	[OrderMonth] [tinyint],
	[FirstOrderYear] [int],
	[LastOrderYear] [int],
	[ProductLine] [nvarchar](50),
	[AddressLine1] [nvarchar](60),
	[AddressLine2] [nvarchar](60),
	[AnnualSales] [money],
	[BankName] [nvarchar](50),
	[MinPaymentType] [tinyint],
	[MinPaymentAmount] [money],
	[AnnualRevenue] [money],
	[YearOpened] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/DimReseller.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimSalesReason')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimSalesReason]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimSalesReason](
	[SalesReasonKey] [int],
	[SalesReasonAlternateKey] [int],
	[SalesReasonName] [nvarchar](50),
	[SalesReasonReasonType] [nvarchar](50)
) WITH (
	LOCATION = 'AdventureWorksDW/DimSalesReason.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimSalesTerritory')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimSalesTerritory]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimSalesTerritory](
	[SalesTerritoryKey] [int],
	[SalesTerritoryAlternateKey] [int],
	[SalesTerritoryRegion] [nvarchar](50),
	[SalesTerritoryCountry] [nvarchar](50),
	[SalesTerritoryGroup] [nvarchar](50),
	[SalesTerritoryImage] [varbinary](max)
) WITH (
	LOCATION = 'AdventureWorksDW/DimSalesTerritory.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'DimScenario')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[DimScenario]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[DimScenario](
	[ScenarioKey] [int],
	[ScenarioName] [nvarchar](50)
) WITH (
	LOCATION = 'AdventureWorksDW/DimScenario.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactAdditionalInternationalProductDescription')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactAdditionalInternationalProductDescription]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactAdditionalInternationalProductDescription](
	[ProductKey] [int],
	[CultureName] [nvarchar](50),
	[ProductDescription] [nvarchar](max)
) WITH (
	LOCATION = 'AdventureWorksDW/FactAdditionalInternationalProductDescription.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactCallCenter')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactCallCenter]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactCallCenter](
	[FactCallCenterID] [int],
	[DateKey] [int],
	[WageType] [nvarchar](15),
	[Shift] [nvarchar](20),
	[LevelOneOperators] [smallint],
	[LevelTwoOperators] [smallint],
	[TotalOperators] [smallint],
	[Calls] [int],
	[AutomaticResponses] [int],
	[Orders] [int],
	[IssuesRaised] [smallint],
	[AverageTimePerIssue] [smallint],
	[ServiceGrade] float,
	[Date] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactCallCenter.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactCurrencyRate')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactCurrencyRate]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactCurrencyRate](
	[CurrencyKey] [int],
	[DateKey] [int],
	[AverageRate] float,
	[EndOfDayRate] float,
	[Date] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactCurrencyRate.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactFinance')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactFinance]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactFinance](
	[FinanceKey] [int],
	[DateKey] [int],
	[OrganizationKey] [int],
	[DepartmentGroupKey] [int],
	[ScenarioKey] [int],
	[AccountKey] [int],
	[Amount] money,
	[Date] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactFinance.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactInternetSales')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactInternetSales]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactInternetSales](
	[ProductKey] [int],
	[OrderDateKey] [int],
	[DueDateKey] [int],
	[ShipDateKey] [int],
	[CustomerKey] [int],
	[PromotionKey] [int],
	[CurrencyKey] [int],
	[SalesTerritoryKey] [int],
	[SalesOrderNumber] [nvarchar](20),
	[SalesOrderLineNumber] [tinyint],
	[RevisionNumber] [tinyint],
	[OrderQuantity] [smallint],
	[UnitPrice] [money],
	[ExtendedAmount] [money],
	[UnitPriceDiscountPct] float,
	[DiscountAmount] money,
	[ProductStandardCost] [money],
	[TotalProductCost] [money],
	[SalesAmount] [money],
	[TaxAmt] [money],
	[Freight] [money],
	[CarrierTrackingNumber] [nvarchar](25),
	[CustomerPONumber] [nvarchar](25),
	[OrderDate] [datetime],
	[DueDate] [datetime],
	[ShipDate] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactInternetSales.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactInternetSalesReason')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactInternetSalesReason]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactInternetSalesReason](
	[SalesOrderNumber] [nvarchar](20),
	[SalesOrderLineNumber] [tinyint],
	[SalesReasonKey] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/FactInternetSalesReason.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactProductInventory')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactProductInventory]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactProductInventory](
	[ProductKey] [int],
	[DateKey] [int],
	[MovementDate] [date],
	[UnitCost] [money],
	[UnitsIn] [int],
	[UnitsOut] [int],
	[UnitsBalance] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/FactProductInventory.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactResellerSales')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactResellerSales]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactResellerSales](
	[ProductKey] [int],
	[OrderDateKey] [int],
	[DueDateKey] [int],
	[ShipDateKey] [int],
	[ResellerKey] [int],
	[EmployeeKey] [int],
	[PromotionKey] [int],
	[CurrencyKey] [int],
	[SalesTerritoryKey] [int],
	[SalesOrderNumber] [nvarchar](20),
	[SalesOrderLineNumber] [tinyint],
	[RevisionNumber] [tinyint],
	[OrderQuantity] [smallint],
	[UnitPrice] [money],
	[ExtendedAmount] [money],
	[UnitPriceDiscountPct] float,
	[DiscountAmount] [money],
	[ProductStandardCost] [money],
	[TotalProductCost] [money],
	[SalesAmount] [money],
	[TaxAmt] [money],
	[Freight] [money],
	[CarrierTrackingNumber] [nvarchar](25),
	[CustomerPONumber] [nvarchar](25),
	[OrderDate] [datetime],
	[DueDate] [datetime],
	[ShipDate] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactResellerSales.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactSalesQuota')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactSalesQuota]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactSalesQuota](
	[SalesQuotaKey] [int],
	[EmployeeKey] [int],
	[DateKey] [int],
	[CalendarYear] [smallint],
	[CalendarQuarter] [tinyint],
	[SalesAmountQuota] [money],
	[Date] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactSalesQuota.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'FactSurveyResponse')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[FactSurveyResponse]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[FactSurveyResponse](
	[SurveyResponseKey] [int],
	[DateKey] [int],
	[CustomerKey] [int],
	[ProductCategoryKey] [int],
	[EnglishProductCategoryName] [nvarchar](50),
	[ProductSubcategoryKey] [int],
	[EnglishProductSubcategoryName] [nvarchar](50),
	[Date] [datetime]
) WITH (
	LOCATION = 'AdventureWorksDW/FactSurveyResponse.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'NewFactCurrencyRate')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[NewFactCurrencyRate]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[NewFactCurrencyRate](
	[AverageRate] [real],
	[CurrencyID] [nvarchar](3),
	[CurrencyDate] [date],
	[EndOfDayRate] [real],
	[CurrencyKey] [int],
	[DateKey] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/NewFactCurrencyRate.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

IF EXISTS (SELECT * FROM sys.external_tables WHERE [name] = 'ProspectiveBuyer')
    DROP EXTERNAL TABLE [AdventureWorksDWStaging].[ProspectiveBuyer]
GO

CREATE EXTERNAL TABLE [AdventureWorksDWStaging].[ProspectiveBuyer](
	[ProspectiveBuyerKey] [int],
	[ProspectAlternateKey] [nvarchar](15),
	[FirstName] [nvarchar](50),
	[MiddleName] [nvarchar](50),
	[LastName] [nvarchar](50),
	[BirthDate] [datetime],
	[MaritalStatus] [nchar](1),
	[Gender] [nvarchar](1),
	[EmailAddress] [nvarchar](50),
	[YearlyIncome] [money],
	[TotalChildren] [tinyint],
	[NumberChildrenAtHome] [tinyint],
	[Education] [nvarchar](40),
	[Occupation] [nvarchar](100),
	[HouseOwnerFlag] [nchar](1),
	[NumberCarsOwned] [tinyint],
	[AddressLine1] [nvarchar](120),
	[AddressLine2] [nvarchar](120),
	[City] [nvarchar](30),
	[StateProvinceCode] [nvarchar](3),
	[PostalCode] [nvarchar](15),
	[Phone] [nvarchar](20),
	[Salutation] [nvarchar](8),
	[Unknown] [int]
) WITH (
	LOCATION = 'AdventureWorksDW/ProspectiveBuyer.csv',
	DATA_SOURCE = [samples_data_lake],
	FILE_FORMAT = [SynapsePipeDelimitedTextFormat]
	)
GO

SELECT TOP 5 * FROM [AdventureWorksDWStaging].[AdventureWorksDWBuildVersion]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimAccount]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimCurrency]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimCustomer]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimDate]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimDepartmentGroup]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimEmployee]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimGeography]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimOrganization]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimProduct]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimProductCategory]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimProductSubcategory]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimPromotion]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimReseller]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimSalesReason]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimSalesTerritory]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[DimScenario]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactAdditionalInternationalProductDescription]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactCallCenter]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactCurrencyRate]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactFinance]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactInternetSales]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactInternetSalesReason]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactProductInventory]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactResellerSales]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactSalesQuota]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[FactSurveyResponse]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[NewFactCurrencyRate]
GO
SELECT TOP 5 * FROM [AdventureWorksDWStaging].[ProspectiveBuyer]
GO