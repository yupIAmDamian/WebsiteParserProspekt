import json

class JsonifyData:
    def __init__(self):
        pass
    
    def writeDataToJson(self, data):
        with open("data.json", "w") as file:
            json.dump(data, file)