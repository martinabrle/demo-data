[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "4dcb26f9-27e5-4575-8d90-e3103a1bd6c1"]}[Data]{[lakehouseId = "2fb1ed56-563d-40a6-8e81-ce5a442cb8a0"]}[Data];
[BindToDefaultDestination = true]
shared sales_json = let
  Source = Lakehouse.Contents([HierarchicalNavigation = null]),
  #"Navigation 1" = Source{[workspaceId = "4dcb26f9-27e5-4575-8d90-e3103a1bd6c1"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "2fb1ed56-563d-40a6-8e81-ce5a442cb8a0"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "Files", ItemKind = "Folder"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[Name = "sales.json"]}[Content],
  #"Imported JSON" = Json.Document(#"Navigation 4"),
  #"Converted to table" = Table.FromList(#"Imported JSON", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to table", "Column1", {"entityType", "Customer_ID", "Product_ID", "Quantity_Sold", "Unit_Price", "Total_Price", "Timestamp"}, {"entityType", "Customer_ID", "Product_ID", "Quantity_Sold", "Unit_Price", "Total_Price", "Timestamp"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Expanded Column1", {{"Timestamp", type text}, {"Total_Price", type number}, {"Unit_Price", type number}, {"Quantity_Sold", Int64.Type}, {"Product_ID", Int64.Type}, {"Customer_ID", Int64.Type}, {"entityType", type text}})
in
  #"Changed column type";
