from Google import Create_Service

CLIENT_SECRET_FILE = 'credientials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

print(dir(service)) #check service working

colours = ['Yellow','Red','Lmao']

for x in colours:
    file_metadata ={
        'name' : x,
        'mimeType' :'application/vnd.google-apps.folder'
        # 'parents' 'testing'
    }

    service.files().create(body=file_metadata).execute()

# from streamlit import caching
# caching.clear_memo_cache()