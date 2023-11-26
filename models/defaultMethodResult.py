# models\defaultMethodResult.py
# Author : Andre Baldo (http://github.com/andrebaldo/)
# A default class to build a default request response
# throught json serialization
class DefaultMethodResult():
    success= False
    message= ''
    data = {}
    def __init__(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data