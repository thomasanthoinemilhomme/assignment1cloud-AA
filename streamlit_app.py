import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# Ensure the path to your service account file is correct and accessible
# Note: When deploying or sharing your app, make sure to securely manage this file
# Avoid hardcoding paths or sensitive data directly in your code for production applications
service_account_file_path = r"C:\Users\tommi\Downloads\crafty-acumen-406617-0a4933a9569d.json"

credentials = service_account.Credentials.from_service_account_file(service_account_file_path)

# Make sure the 'project' argument is set to your Google Cloud project ID
# This is a string, for example: 'my-gcp-project-id'
client = bigquery.Client(credentials=credentials, project='crafty-acumen-406617')
