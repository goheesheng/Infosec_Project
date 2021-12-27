import os

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
        
    return (allFiles)

a = getListOfFiles("C:\\Users\\Gaming-Pro\\OneDrive\\Desktop\\Drive_test")

print(a)

# for root, directories, files in os.walk(a, topdown=True):
#     for name in files:
#         print(os.path.join(root, name))
#     for name in directories:
#         print(root,'root')
#         print(os.path.join(root, name))