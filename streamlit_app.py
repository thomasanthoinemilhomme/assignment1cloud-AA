pip install streamlit google-cloud-bigquery

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('path/to/your/service-account-file.json')
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

