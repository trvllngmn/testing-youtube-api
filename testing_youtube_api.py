import os
import sys
from pprint import pprint
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Load stored environment variables from '.env'
load_dotenv()

# Constants
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILEPATH')
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
l_of_report_types = reporting_api.reportTypes().list(
    onBehalfOfContentOwner=CONTENT_ID
).execute()

## List scheduled jobs, created after: 2024-04-27:
created_after = '2024-04-27T00:00:00.00Z'

l_of_scheduled_reporting_jobs = reporting_api.jobs().list(
    onBehalfOfContentOwner=CONTENT_ID
    ,createdAfter = created_after
).execute()

## View response in terminal
pprint(l_of_scheduled_reporting_jobs)

## Retrieve report's download link:
# job_id = l_of_scheduled_reporting_jobs['']

## Download file:
## TODO
