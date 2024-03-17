
import os
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from google.colab import auth
auth.authenticate_user()

credentials = service_account.Credentials.from_service_account_file('"C:\Users\tommi\Downloads\crafty-acumen-406617-0a4933a9569d.json"')
client = bigquery.Client(credentials=credentials, project=credentials.crafty-acumen-406617)

