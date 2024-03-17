import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import json

# Assuming the service account JSON is passed as a string in the environment variable
credentials_raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if credentials_raw:
    credentials_dict = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
else:
    st.error("Google Cloud credentials not provided.")
    st.stop()
