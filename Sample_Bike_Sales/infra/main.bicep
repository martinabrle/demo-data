targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment (used to generate a short unique hash for resources).')
param environmentName string

@minLength(1)
@description('Primary location for all resources.')
param location string

@description('Microsoft Entra ID tenant ID for JWT validation. Leave empty to disable auth.')
param azureTenantId string = ''

@description('Microsoft Entra ID app registration client ID. Leave empty to disable auth.')
param azureClientId string = ''

@description('API audience (typically api://<client-id>). Defaults to azureClientId.')
param azureApiAudience string = ''

// ── derived names ───────────────────────────────────────────────────────────
var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// ── resource group ──────────────────────────────────────────────────────────
resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// ── app service (plan + web app) ────────────────────────────────────────────
module appService './modules/app-service.bicep' = {
  name: 'app-service'
  scope: rg
  params: {
    location: location
    tags: tags
    appServicePlanName: '${abbrs.webServerFarms}${resourceToken}'
    appServiceName: '${abbrs.webSitesAppService}${resourceToken}'
    appSettings: {
      AZURE_TENANT_ID: azureTenantId
      AZURE_CLIENT_ID: azureClientId
      AZURE_API_AUDIENCE: !empty(azureApiAudience) ? azureApiAudience : azureClientId
      CSV_DATA_DIR: './data'
      SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
    }
  }
}

// ── outputs (consumed by azd) ───────────────────────────────────────────────
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = azureTenantId
output SERVICE_API_NAME string = appService.outputs.appServiceName
output SERVICE_API_URI string = appService.outputs.uri
