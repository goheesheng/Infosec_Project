import os    
    
    
# Update to Google Drive
folder_path = "C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\SQL BACKUP\\"
folders = os.listdir(folder_path) #['folder1', 'folder2'] list folder

print(folders[-1])