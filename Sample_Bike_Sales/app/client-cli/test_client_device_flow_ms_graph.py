"""
A Python application that demonstrates how to use the
Device Code flow to make an API call to Microsoft Graph.
"""

import json
import os
from pathlib import Path

# Microsoft Authentication Library (MSAL) for Python
import msal

# Used to allow the app to make the HTTP request to Graph
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")  # App registration client-id

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

# Initialize the Device Code flow for the necessary scope(s) - in Graph
deviceFlow = msalClientApp.initiate_device_flow(scopes=["User.Read"])

if "message" not in deviceFlow:
    raise RuntimeError(f"Failed to start device flow: {deviceFlow}")

# Displays a message instructing the user to authenticate via their browser
print(deviceFlow["message"], flush=True)

# Get the Graph access token from MSAL
msalResponse = msalClientApp.acquire_token_by_device_flow(deviceFlow)

print("\nMSAL response - Graph:")
print(json.dumps(msalResponse, indent=2))
print("\n")

if "access_token" in msalResponse:
    # Make an HTTP GET request to the Graph API using the access token and display the response
    print("Making an authenticated API call to Microsoft Graph /me endpoint...")
    print(
        json.dumps(
            requests.get("https://graph.microsoft.com/v1.0/me", headers={"Authorization": "Bearer " + msalResponse["access_token"]},).json(),
            indent=2
        )
    )
else:
    raise RuntimeError(f"Authentication failed: {msalResponse.get('error_description')}")
