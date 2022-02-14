import subprocess

# def psrun(cmd):
#     completed = subprocess.Popen(["powershell", "-Command", cmd], shell=True ,stdout=subprocess.PIPE,universal_newlines=True,stderr=subprocess.PIPE)
#     return completed


# if __name__ == "__main__":

#     out=' '
#     for s in psrun(" Get-Service 'MSSQLSERVER' | Format-List -Property Status").stderr:
#         out+=s

#     for s in psrun(" Get-Service 'MSSQLSERVER' | Format-List -Property Status").stdout:
#         out+=s

#     print(out.strip())

#     if 'Stopped' in out.strip():
#         print('ur mum')    

#     else:
#         print('no mum')



def psrun(cmd):
    completed = subprocess.Popen(["powershell", cmd],stdout=subprocess.PIPE)
    return completed
if __name__ == "__main__":
    x=psrun("Get-Service 'MSSQLSERVER' | Select-Object -Property Status").stdout.read()
    if b"Stopped" in x:
        print('hi')