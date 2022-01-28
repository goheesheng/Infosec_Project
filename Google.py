import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
<<<<<<< Updated upstream
=======
from apiclient.http import MediaFileUpload
from mssql_auth import database, server
from glob import glob
import os
import pyodbc
import time



class MyDrive():
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def list_files(self, page_size=10):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        fileid_list = []
        if not items:
            print('No files found.')
        else:
            print('Files:')
            # print('items',items)
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
                fileid_list.append(item['id'])
            print(fileid_list)
            return fileid_list

    def create_file(self, filename, path,connection):
        folder_id = "1gXysKHVy8QXGKs-rhSLwDpnW9O3Gkh-_" #is on google drive URL, this is the folder id of ISPJ Backup
        
        media = MediaFileUpload(f"{path}{filename}")

        response = self.service.files().list(
                                        q=f"name='{filename}' and parents='{folder_id}'", #parents is to ensure that if there is a duplicate name folder in drive
                                        spaces='drive',                                   #we do not want to upload to that file but the file we want thus use the folder_id
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=None).execute()
        print(response)
        if len(response['files']) == 0: #To create the filed in drive if not created
            file_metadata = {
                'name': filename,
                'parents': [folder_id] #need to pass  as list
            }
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"A new file was created {file.get('id')}")

            t = time.localtime()
            current_time = str(time.strftime("%d %B %Y_%H;%M;%S",t)) #e.g 30 December 2021_21;20;28 hour minute second
>>>>>>> Stashed changes


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt