import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googlesearch import search
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
from mssql_auth import database, server
from glob import glob
import os
import pyodbc
import time
import io



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

    def last_file(self, page_size=10):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        fileid_list = []
        if not items:
            print('No files found.')
        else:
            print('Files found in drive')
            # print('items',items)
            fileid_list.append(items[0]['name'])
            fileid_list.append(items[0]['id'])
            # for item in items:
            #     print(u'{0} ({1})'.format(item['name'], item['id']))
            #     fileid_dict[item['id']]=item['name']
            # print(fileid_list[0])
            return fileid_list

    def download_file(self,file_id):
        
    
        request = self.service.files().get_media(fileId=file_id[1])
        fh=io.FileIO(f"C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\{file_id[0]}",'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        

   

    def create_file(self, filename, path):
        folder_id = "1gXysKHVy8QXGKs-rhSLwDpnW9O3Gkh-_" #is on google drive URL
        
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

            # cnxn = pyodbc.connect(
            # 'DRIVER={ODBC Driver 17 for SQL Server}; \
            # SERVER=' + 'GOHDESKTOP\SQLEXPRESS' + '; \
            # DATABASE=' + 'database1' + ';\
            # Trusted_Connection=yes;'
            # )
        #     cursor = connection


        #     sql_backup = "INSERT INTO google(folder_id, backup_date) VALUES (?, ?)"
        #     parameters = (file.get('id'),current_time)
        #     cursor.execute(sql_backup, parameters)
        #     cursor.commit()
        #     print('update google table')
        # else: # To update files in drive
        #     pass
        #     # for file in response.get('files', []):
        #     #     # Process change
        #     #
        #     #     update_file = self.service.files().update(
        #     #         fileId=file.get('id'),
        #     #         media_body=media,
        #     #     ).execute()
        #     #     print(f'Updated File')


def main():
    folder_path = "C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\"
    folders = os.listdir(folder_path) #['folder1', 'folder2'] list folder
    # folder_list = []
    # for folder in folders:
    #     file_path = os.listdir("C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\Drive_test\\" + folder) #['folder1.txt', 'folder11.txt'] list text
    #     folder_list.append(folder)
    #     print(folder_list)
        
    my_drive = MyDrive()
    # # my_drive.list_files() #to check api working

    # for folder in folder_list:
    #     print(folder,'folder')
    #     my_drive.create_folder(folder,folder_path)
    # cnxn = pyodbc.connect(
    #     'DRIVER={ODBC Driver 17 for SQL Server}; \
    #     SERVER=' + server + '; \
    #     DATABASE=' + database + ';\
    #     Trusted_Connection=yes;'
    #     )
    # cursor = cnxn.cursor()

    # folder_path = cursor.execute("select * from google").fetchall()
    # print(folder_path)


    last_file= my_drive.last_file()
    my_drive.download_file(last_file)
    # for folder in folders:
    #     my_drive.create_file(folder, folder_path)

    # cursor.close()


if __name__ == '__main__':

    main()

