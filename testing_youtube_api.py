import os
import sys
from io import FileIO
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

def download_report(api, report):
    """Call the YouTube Reporting API's media.download method to download the report.
    """
    request = api.media().download(resourceName='csv')
    request.uri = report['downloadUrl']
    report_name = f'reportId-'+report['id']+'-'+report['startTime'][0:10]+'-to-'+report['endTime'][0:10]+'.csv'

    print(f"--> Downloading: " + report_name)
    
    fh = FileIO(report_name, mode='wb')
    # Stream/download the report in a single request.
    downloader = MediaIoBaseDownload(fh, request, chunksize=-1)
    
    done = False
    
    while done is False:
        status, done = downloader.next_chunk()
    if status:
        print('Download %d%%.' % int(status.progress() * 100))
    
    print('--> Download Complete!')

# Authenticate with YouTube Reporting service
reporting_api = get_authenticated_service()

## List available report types:
l_of_report_types = reporting_api.reportTypes().list(
    onBehalfOfContentOwner=CONTENT_ID
).execute()

## List scheduled jobs, created after: 2024-04-27:
created_after = '2024-04-27T00:00:00.00Z'
job_id = '93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3'

# Comment this section once we have info for missing report
response = reporting_api.jobs().reports().list(
    onBehalfOfContentOwner=CONTENT_ID
    ,jobId = job_id
    ,createdAfter = created_after
).execute()

pprint(response)

# Exit script early to capture response - comment out below once we have
sys.exit()

## Download file:
missing_report = {
    "id": None,
    "startTime": None,
    "endTime": None,
    "createTime": None,
    "downloadUrl": None
}

reports = [
    ,{"id": "10431303585",  "startTime": "2024-04-25T07:00:00Z", "endTime": "2024-04-26T07:00:00Z", "createTime": "2024-04-29T16:45:18.349494Z", "downloadUrl": f"https://youtubereporting.googleapis.com/v1/media/CONTENT_OWNER/{CONTENT_ID}/jobs/93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3/reports/10431303585?alt=media"}
    ,{"id": "10843545654",  "startTime": "2024-04-25T07:00:00Z", "endTime": "2024-04-26T07:00:00Z", "createTime": "2024-04-27T08:00:17.956838Z", "downloadUrl": f"https://youtubereporting.googleapis.com/v1/media/CONTENT_OWNER/{CONTENT_ID}/jobs/93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3/reports/10843545654?alt=media"}
    ,{"id": "10417327321",  "startTime": "2024-04-18T07:00:00Z", "endTime": "2024-04-19T07:00:00Z", "createTime": "2024-04-24T06:54:03.775379Z", "downloadUrl": f"https://youtubereporting.googleapis.com/v1/media/CONTENT_OWNER/{CONTENT_ID}/jobs/93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3/reports/10417327321?alt=media"}
    ,{"id": "10415711308",  "startTime": "2024-04-18T07:00:00Z", "endTime": "2024-04-19T07:00:00Z", "createTime": "2024-04-23T21:50:53.881200Z", "downloadUrl": f"https://youtubereporting.googleapis.com/v1/media/CONTENT_OWNER/{CONTENT_ID}/jobs/93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3/reports/10415711308?alt=media"}
    ,{"id": "10814486324",  "startTime": "2024-04-18T07:00:00Z", "endTime": "2024-04-19T07:00:00Z", "createTime": "2024-04-20T05:52:22.201216Z", "downloadUrl": f"https://youtubereporting.googleapis.com/v1/media/CONTENT_OWNER/{CONTENT_ID}/jobs/93bd5ae9-d9bc-4f2f-a48e-da0a7353e7f3/reports/10814486324?alt=media"}
    ,missing_report
]

# Call downlod_func per report
for report in reports:
    download_report(reporting_api, report)
    print('--> End of script')
