class StringUtility(object):
    
    @staticmethod
    def length(string):
        return len(string)

class FileUtility(object):
 
    @staticmethod
    def open(path):
        print("Opened " + path + ".")
 
    @staticmethod
    def open_json(path):
        print("Opened " + path + " JSON.")