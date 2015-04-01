import base64
import json


def file_to_json(filename, meta={}):
    result = dict(meta)
    with open(filename, "rb") as file:
        data = file.read()
        result["data"] = base64.b64encode(data)
        result["filename"] = filename
    return json.dumps(result)


def json_to_file(file_json, new_file_name=None):
    json_dict = json.loads(file_json)
    dict_to_file(json_dict,new_file_name)

def dict_to_file(file_dict, new_file_name=None):
    if file_dict.get("data",None) == None:
        print "No data in json!"
        return
    data = base64.b64decode(file_dict["data"])
    if new_file_name is not None:
        fileName = new_file_name
    else:
        fileName = file_dict["filename"]
    with open(fileName, "wb+") as file:
        file.write(data)


if __name__ == '__main__':
    buddy = file_to_json("image.jpg")
    json_to_file(buddy, "image2.jpg")
