import logging

import csv
import os

class patientFileModificationFilter(logging.Filter):
    def __init__(self, ipaddress, username):
        self.ipaddress = ipaddress
        self.username = username

    def filter(self, record):
        record.ipaddress = self.ipaddress
        record.username = self.username
        return True


#everything in the class arguements apart from level,acstime and message fields
class db_log(logging.Filter):
    def __init__(self,server):
        self.server = server

    def filter(self, record):
        record.server = self.server

        return True

class lr_log(logging.Filter): #login, register
    def __init__(self, username):
        self.username = username

    def filter(self, record):
        record.username = self.username
        return True

class ac_log(logging.Filter): #access control
    def __init__(self,page_visited,ipaddress,username):
        self.page_visited = page_visited
        self.ipaddress = ipaddress
        self.username = username

    def filter(self, record):
        record.page_visited = self.page_visited
        record.ipaddress = self.ipaddress
        record.username = self.username

        return True


class virus_log(logging.Filter): #login, register, access control
    def __init__(self, username,ipaddress):
        self.username = username
        self.ipaddress = ipaddress
        
    def filter(self, record):
        record.username = self.username
        record.ipaddress = self.ipaddress


        return True
        


def converTxtToCSV():
    patient_file_log_field=['Time','Level','Message','IP Address','Username']
    login_reigister_log_field=['Time','Level','Username','Message']
    access_control_log_field=['Time','Level','Message','IP Address','Username','Page visited']
    db_log_field=['Time','Level','Message']
    virus_log_field=['Time','Level','Message','IP Address','Username']

    patient_file_log_file="logs/patientFileChangelog"
    login_register_log_file="logs/lr_logs"
    db_log_file="logs/db_logs"
    access_control_log_file="logs/ac_logs"
    virus_log_file="logs/virus_logs"

    patient_file_log_file_text=patient_file_log_file+".txt"
    patient_file_log_file_csv="logs/csv_logs/patientFileChangelog"+".csv"

    login_register_log_txt=login_register_log_file+".txt"
    login_register_log_file_csv="logs/csv_logs/lr_log"+".csv"

    db_file_txt=db_log_file+".txt"
    db_file_csv="logs/csv_logs/db_logs"+".csv"

    access_control_log_file_text=access_control_log_file+".txt"
    access_control_log_file_csv="logs/csv_logs/ac_logs"+".csv"

    virus_log_file_txt=virus_log_file+".txt"
    virus_log_file_csv="logs/csv_logs/virus_logs"+".csv"

    list_of_text_files=[patient_file_log_file_text,login_register_log_txt,db_file_txt,access_control_log_file_text,virus_log_file_txt]
    list_of_csv_files=[patient_file_log_file_csv,login_register_log_file_csv,db_file_csv,access_control_log_file_csv,virus_log_file_csv]
    list_of_fields=[patient_file_log_field,login_reigister_log_field,db_log_field,access_control_log_field,virus_log_field]

    def convert_csv(log_file,output_file,fields):
        in_txt=csv.reader(open(log_file,"r"),delimiter=";")
        out_txt=csv.writer(open(output_file,'w'))
        out_txt.writerow(fields)
        out_txt.writerows(in_txt)


    for index in range(len(list_of_text_files)):
        print(list_of_text_files[index],list_of_csv_files[index],list_of_fields[index])
        convert_csv(list_of_text_files[index],list_of_csv_files[index],list_of_fields[index])

if __name__=="__main__":
    converTxtToCSV()