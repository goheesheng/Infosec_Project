import base64        
### Function to decode the message.
def decode(string):
    

    ### Get each word and store in list
    list_words = string.split()
    # print(each_words)

    # Store the decoded string
    res = ""


    for word in list_words:
        print(word[-1])
        res += word[-1]
    
    return res.upper()

# Driver code
if __name__ == "__main__":
    input = "Sm9objogV2hhdOKAmVMgVGhhdD8gU2FtdWVsOiBMb2wgQW4gT3Bwb3J0dW5pc3RpYyAxMjIyIDEwMDAgMjIxMiA0MTMyIFBlcnNvbnsgSXMgU29sdmluZyBUaGlzIEVhc3kgTnVsbCBDdGYgQ2hhbGxlbmdlfSBKb2huOldvdyBJdCBJcyBSZWFsbHkgRWFzeS4="
    decoded_string = base64.b64decode(input)
    string = decoded_string.decode("utf-8")
    # print(string)
    # print(type(string))
    print("Decoded Cipher Text:",decode(string))