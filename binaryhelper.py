import base64
import json

def file_to_json(filename, meta):
    result = dict(meta)
    with open(filename, "rb") as file:
        data = file.read()
        result["data"] = base64.b64encode(data)
        result["filename"] = filename
    return json.dumps(result)

def json_to_file(file_json, new_file_name = None):
    json_dict = json.loads(file_json)
    data = base64.b64decode(json_dict["data"])
    if new_file_name is not None:
        fileName = new_file_name
    else:
        fileName = json_dict["filename"]
    with open(fileName, "wb+") as file:
        file.write(data)


if __name__ == '__main__':
    buddy = file_to_json("bud.jpg")
    json_to_file(buddy, "buddy.jpg")