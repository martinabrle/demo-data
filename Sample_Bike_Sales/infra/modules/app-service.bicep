// ── App Service Plan + Web App ───────────────────────────────────────────────
@description('Location for all resources.')
param location string

param tags object = {}

@description('Name for the App Service Plan.')
param appServicePlanName string

@description('Name for the App Service (web app).')
param appServiceName string

@description('App Service SKU.')
param sku string = 'B1'

@description('Application settings (env vars) for the web app.')
param appSettings object = {}

// ── App Service Plan ────────────────────────────────────────────────────────
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: sku
  }
  properties: {
    reserved: true // required for Linux
  }
}

// ── Web App ─────────────────────────────────────────────────────────────────
resource appService 'Microsoft.Web/sites@2023-12-01' = {
  name: appServiceName
  location: location
  tags: union(tags, { 'azd-service-name': 'api' })
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      alwaysOn: true
      ftpsState: 'Disabled'
      appCommandLine: 'pip install -r requirements.txt && gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120'
      appSettings: [for key in objectKeys(appSettings): {
        name: key
        value: appSettings[key]
      }]
    }
  }
}

output appServiceName string = appService.name
output uri string = 'https://${appService.properties.defaultHostName}'
