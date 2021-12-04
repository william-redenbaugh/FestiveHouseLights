import json

def parse_input_json(message_bytearray) 
    str_message = message_bytearray.decode(message_bytearray)
    data = None
    try: 
        data = json.loads(str_message)
    except:
        print("Message does not come in JSON format")
        return None
    return data 


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True 