# Bike Sales Mock API

A **FastAPI**-based mock REST API that serves the Sample Bike Sales CSV data
entirely from an in-memory store. The API is protected by **Microsoft Entra ID**
(Azure AD) via JWT validation using the `PyJWT` library.

---

## Quick start (local)

```bash
cd Sample_Bike_Sales/app/api

# create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# (optional) copy and fill in auth settings
cp .env.sample .env

# run the dev server
uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000/docs> for the interactive Swagger UI.

> **Note:** When `AZURE_TENANT_ID` and `AZURE_CLIENT_ID` are not set the API
> runs with authentication **disabled** (all endpoints are open).

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health / service info |
| `GET` | `/health` | Health check |
| `GET` | `/products` | List products (filterable by `category`) |
| `GET` | `/products/{id}` | Get product by ID |
| `PATCH` | `/products/{id}` | Update product fields in memory |
| `DELETE` | `/products/{id}` | Delete product in memory |
| `GET` | `/products/{id}/page` | Get product page markdown |
| `GET` | `/products/{id}/texts` | Get product descriptions |
| `GET` | `/product-categories` | List product categories |
| `GET` | `/product-categories/{id}` | Get category by ID |
| `PATCH` | `/product-categories/{id}` | Update category fields in memory |
| `DELETE` | `/product-categories/{id}` | Delete category in memory |
| `GET` | `/product-categories/{id}/texts` | Category description texts |
| `PATCH` | `/product-categories/{id}/texts?language=EN` | Update category text fields in memory |
| `DELETE` | `/product-categories/{id}/texts?language=EN` | Delete category text in memory |
| `GET` | `/product-categories/{id}/products` | Products in a category |
| `GET` | `/customers` | List customers |
| `GET` | `/customers/{id}` | Get customer by ID |
| `PATCH` | `/customers/{id}` | Update customer fields in memory |
| `DELETE` | `/customers/{id}` | Delete customer in memory |
| `GET` | `/customers/{id}/orders` | Orders placed by a customer |
| `GET` | `/addresses` | List addresses (filterable by `country`) |
| `GET` | `/addresses/{id}` | Get address by ID |
| `PATCH` | `/addresses/{id}` | Update address fields in memory |
| `DELETE` | `/addresses/{id}` | Delete address in memory |
| `GET` | `/employees` | List employees |
| `GET` | `/employees/{id}` | Get employee by ID |
| `PATCH` | `/employees/{id}` | Update employee fields in memory |
| `DELETE` | `/employees/{id}` | Delete employee in memory |
| `GET` | `/vendors` | List vendors |
| `GET` | `/vendors/{id}` | Get vendor by ID |
| `PATCH` | `/vendors/{id}` | Update vendor fields in memory |
| `DELETE` | `/vendors/{id}` | Delete vendor in memory |
| `GET` | `/sales-orders` | List sales orders |
| `GET` | `/sales-orders/{id}` | Get sales order by ID |
| `PATCH` | `/sales-orders/{id}` | Update sales order fields in memory |
| `DELETE` | `/sales-orders/{id}` | Delete sales order in memory |
| `GET` | `/sales-orders/{id}/items` | Line items for an order |
| `PATCH` | `/sales-orders/{id}/items/{itemId}` | Update sales order item fields in memory |
| `DELETE` | `/sales-orders/{id}/items/{itemId}` | Delete sales order item in memory |

All list endpoints support `skip` and `limit` query parameters for pagination.

Product and sales order write operations in this demo API are in-memory only and are reset when the app restarts.

---

## Authentication (Microsoft Entra ID)

Set these environment variables (or App Service configuration) to enable:

| Variable | Description |
|----------|-------------|
| `AZURE_TENANT_ID` | Your Entra ID tenant ID |
| `AZURE_CLIENT_ID` | App registration client / application ID |
| `AZURE_API_AUDIENCE` | API audience URI (defaults to `AZURE_CLIENT_ID`) |

The API validates the `Authorization: Bearer <token>` header against the
tenant's OIDC `jwks_uri`, checking `exp`, `iss`, and `aud` claims.

---

## Deploy to Azure (azd)

The project includes an [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
template that provisions an **App Service (Linux, B1)** and deploys the API.

```bash
cd Sample_Bike_Sales

# first time
azd init

# provision infra + deploy
azd up
```

You'll be prompted for `environmentName` and `location`. Optionally set the
Entra ID parameters:

```bash
azd env set AZURE_TENANT_ID   <tenant-id>
azd env set AZURE_CLIENT_ID   <client-id>
azd env set AZURE_API_AUDIENCE api://<client-id>
azd up
```

### What gets created

| Resource | Purpose |
|----------|---------|
| Resource Group (`rg-<env>`) | Container for all resources |
| App Service Plan (`plan-<token>`) | Linux B1 plan |
| App Service (`app-<token>`) | Hosts the FastAPI application (Python 3.12) |

---

## Architecture

```
Sample_Bike_Sales/
├── *.csv                    # Source data (10 CSV files)
├── azure.yaml               # azd project descriptor
├── infra/
│   ├── main.bicep           # Subscription-scoped orchestrator
│   ├── main.parameters.json
│   ├── abbreviations.json
│   └── modules/
│       └── app-service.bicep
└── app/api/
    ├── requirements.txt
    ├── .env.sample
    └── app/
        ├── __init__.py
        ├── main.py           # FastAPI application
        ├── auth.py           # Entra ID JWT validation
        ├── datastore.py      # In-memory CSV store
        └── routers/
            ├── products.py
            ├── categories.py
            ├── customers.py
            ├── addresses.py
            ├── employees.py
            ├── vendors.py
            └── sales_orders.py
```
