from re import X
from virustotal_python import Virustotal
import os.path,base64
from pprint import pprint

from forms import Otp # pprint is used to pretty print in good json format instead of in a line
# # v2 example
# vtotal = Virustotal(API_KEY="Insert API key here.")

# v3 example
vtotal = Virustotal(API_KEY="<key>", API_VERSION="v3")

# print(vtotal)

def virusTotal(vtotal,filepath):

    # You can provide True to the `COMPATIBILITY_ENABLED` parameter to preserve the old response format of virustotal-python versions prior to 0.1.0
    # vtotal = Virustotal(API_KEY="Insert API key here.", API_VERSION="v3", COMPATIBILITY_ENABLED=True)

    # You can also set proxies and timeouts for requests made by the library
    # vtotal = Virustotal(
    #     API_KEY="Insert API key here.",
    #     API_VERSION="v3",
    #     PROXIES={"http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080"},
    #     TIMEOUT=5.0)

    # As of version 0.1.1, the Virustotal class can be invoked as a Context Manager!
    ## v2 example
    # with Virustotal(API_KEY="Insert API key here.") as vtotal:
    #     # Your code here

    # ## v3 example
    # with Virustotal(API_KEY="Insert API key here.", API_VERSION="v3") as vtotal:
    #     # Your code here

    # print(vtotal)




    # Declare PATH to file
    FILE_PATH = filepath

    # Create dictionary containing the file to send for multipart encoding upload
    files = {"file": (os.path.basename(FILE_PATH), open(os.path.abspath(FILE_PATH), "rb"))}

    # # v2 example
    # resp = vtotal.request("file/scan", files=files, method="POST")

    # # The v2 API returns a response_code
    # # This property retrieves it from the JSON response
    # print(resp.response_code)
    # # Print JSON response from the API
    # pprint(resp.json())

    # v3 example
    resp = vtotal.request("files", files=files, method="POST")

    # The v3 API returns the JSON response inside the 'data' key
    # https://developers.virustotal.com/v3.0/reference#api-responses
    # This property retrieves the structure inside 'data' from the JSON response
    # {'id': 'YmI5ZTFmZjNlMDUwMTQ2NmZkZDcxMDRhYmE0MGVlOTY6MTY0MTQ0Njg0NQ==', 'type': 'analysis'}
    # pprint(resp.data)

    pprint(resp.data['id']) #Id contains bb9e1ff3e0501466fdd7104aba40ee96:1641448194, there is a colon and the numbers are 'first_submission_date': 1641449084 so need to split them
    decode_fileid = base64.b64decode(resp.data['id']).decode('utf-8')
    colon = ':'
    if colon in decode_fileid:
        base64_decoded_id = decode_fileid.split(':')[0]
    else:
        base64_decoded_id = decode_fileid.split('-')[0]
        print('except')
    print(base64_decoded_id,'decode')

    # # Or if you provided COMPATIBILITY_ENABLED=True to the Virustotal class
    # # pprint(resp["json_resp"])

    # v3 example
    resp = vtotal.request(f"files/{base64_decoded_id}")

    pprint(resp.data)

    # https://developers.virustotal.com/reference/analyses-object
    #category: <string> normalised result. Possible values are:
    # "confirmed-timeout" (AV reached a timeout when analysing that file. Only returned in file analyses.)
    # "failure" (AV failed when analysing this file. Only returned in file analyses).
    # "harmless" (AV thinks the file is not malicious),
    # "undetected" (AV has no opinion about this file),
    # "suspicious" (AV thinks the file is suspicious),
    # "malicious" (AV thinks the file is malicious).
    # "type-unsupported" (AV can't analyse that file. Only returned in file analyses).
    pprint(resp.data['attributes']['last_analysis_stats']['malicious']) 

    if resp.data['attributes']['last_analysis_stats']['malicious'] > 0:
        return True
    else:
        return False

# if __name__ == "__main__":

#     if virusTotal(vtotal,'saved\\virus.txt') is False:

#         print('This file is clean!')
#     else:
#         print('This file is malicious!')


