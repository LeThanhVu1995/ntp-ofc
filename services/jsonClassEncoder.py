# services\jsonClassEncoder.py
# Author : Andre Baldo (http://github.com/andrebaldo/)
# A default encoder, it will read the class properties and retur it as a dictionary, 
# so the json serializer can convert it
from json import JSONEncoder
from bson import ObjectId
class JsonClassEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)