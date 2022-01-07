import base64

string = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f-1641537710"
decode_fileid = base64.b64decode(string).decode('utf-8')
print(string.split(':'))

base = string.split(':')[0]
print(base)