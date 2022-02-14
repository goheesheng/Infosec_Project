import json, requests, subprocess, shlex


def execute_request():
    bashCommand = '''curl --request POST 
	--url https://lambda-face-recognition.p.rapidapi.com/recognize 
	--header 'content-type: multipart/form-data; boundary=---011000010111000001101001' 
	--header 'x-rapidapi-host: lambda-face-recognition.p.rapidapi.com' 
	--header 'x-rapidapi-key: 59bfe4aab4mshd7aecd4bc8f59b0p1e6583jsnbd25bc3a99ab' 
	--form files=@photo.jpg 
	--form albumkey=d69607ae3dd0df917ad9c2ace7ddcb7c4135b4f421782316946f7cda24362ff8 
	--form album=admins'''
    args = shlex.split(bashCommand)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, error = process.communicate()
    json_obj = json.loads(output)
    return json_obj


def check_confidence(json_obj):
    if json_obj['status'] == 'success':
        if len(json_obj['photos'][0]['tags']) == 0:
            return False
        confidence = json_obj['photos'][0]['tags'][0]['confidence']
        flag = False
        if confidence > 0.5:
            flag = True
        return flag


def train_face(user_id):
    bashCommand = '''curl --request POST 
	--url https://lambda-face-recognition.p.rapidapi.com/album_train 
	--header 'content-type: multipart/form-data; boundary=---011000010111000001101001' 
	--header 'x-rapidapi-host: lambda-face-recognition.p.rapidapi.com' 
	--header 'x-rapidapi-key: 59bfe4aab4mshd7aecd4bc8f59b0p1e6583jsnbd25bc3a99ab' 
	--form files=@photo.jpg 
	--form entryid='''+user_id+''' 
	--form albumkey=d69607ae3dd0df917ad9c2ace7ddcb7c4135b4f421782316946f7cda24362ff8 
	--form album=admins'''
    args = shlex.split(bashCommand)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, error = process.communicate()
    json_obj = json.loads(output)
    return json_obj
