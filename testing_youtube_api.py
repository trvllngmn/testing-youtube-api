import os
from pprint import pprint
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Load stored environment variables from '.env'
load_dotenv()

# Constants
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE_PATH')
CONTENT_ID = os.getenv('CONTENT_ID')
SCOPES = ['https://www.googleapis.com/auth/yt-analytics-monetary.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'

# Funcs
def get_authenticated_service():
    """Authorize the request and store authorization credentials.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = 'http://localhost:8080'
    flow.run_local_server()

    return build(API_SERVICE_NAME, API_VERSION, credentials = flow.credentials)

def download_report():
    """Call the YouTube Reporting API's media.download method to download the report.
    """
    # TODO
    pass

# Authenticate with YouTube Reporting service
reporting_api = get_authenticated_service()

## List available report types:
l_of_report_types = reporting_api.reportTypes().list(onBehalfOfContentOwner=CONTENT_ID).execute()
pprint(l_of_report_types)

## List scheduled jobs:
l_of_scheduled_reporting_jobs = reporting_api.jobs().list().execute()

## Retrieve report's download link:
job_id = ''
created_after = '' # TODO
download_url = reporting_api.jobs().reports().list(jobId=job_id, createdAfter=created_after).execute()

## Download file:
## TODO