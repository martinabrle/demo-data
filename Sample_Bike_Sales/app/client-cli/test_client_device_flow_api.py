"""
A Python application that demonstrates how to use the
Device Code flow to make an API call to an API.
"""

import json
import os
from pathlib import Path
import base64

# Microsoft Authentication Library (MSAL) for Python
import msal

# Used to allow the app to make the HTTP request to Graph
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")  # App registration client-id
API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
API_SCOPE: str = os.getenv("AZURE_API_SCOPE", "")

# MSAL configs
config = {
    # Full directory URL, in the form of https://login.microsoftonline.com/<tenant_id>
    "authority": f"https://login.microsoftonline.com/{TENANT_ID}",
    # 'Application (client) ID' of app registration in the Microsoft Entra admin center - this value is a GUID
    "client_id": f"{CLIENT_ID}",
}

# Create a MSAL public client application
msalClientApp = msal.PublicClientApplication(
    config["client_id"], authority=config["authority"]
)


def decode_token(token: str) -> dict:
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))

# Initialize the Device Code flow for the necessary API scope
deviceFlow = msalClientApp.initiate_device_flow(scopes=[API_SCOPE])

if "message" not in deviceFlow:
    raise RuntimeError(f"Failed to start device flow: {deviceFlow}")

# Displays a message instructing the user to authenticate via their browser
print(deviceFlow["message"], flush=True)

# Get the Graph access token from MSAL
msalResponse = msalClientApp.acquire_token_by_device_flow(deviceFlow)

print("\nMSAL response:")
print(json.dumps(msalResponse, indent=2))
print("\n")

if "access_token" in msalResponse:
    print("Decoded access token:")
    print(json.dumps(decode_token(msalResponse["access_token"]), indent=2))
    print("\n")
    # Make an HTTP GET request to the API using the access token and display the response
    print(f"Making an authenticated API call to {API_BASE_URL.rstrip('/')}/products ...")
    print(
        json.dumps(
            requests.get(f"{API_BASE_URL.rstrip('/')}/products?limit=3", headers={"Authorization": "Bearer " + msalResponse["access_token"]},).json(),
            indent=2
        )
    )
else:
    raise RuntimeError(f"Authentication failed: {msalResponse.get('error_description')}")
