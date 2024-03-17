import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import base64
import json

# Decode the service account key from the environment variable
base64_credentials = os.getenv("GOOGLE_CREDENTIALS")
decoded_credentials = base64.b64decode(base64_credentials)

# Load the service account info from the decoded JSON string
service_account_info = json.loads(decoded_credentials)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Initialize the BigQuery client with the credentials
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

