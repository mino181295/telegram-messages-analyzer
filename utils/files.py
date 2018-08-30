import os

class FileUtility(object):
 
    @staticmethod
    def file_extension(filename):
        if '.' in filename:
            _, extension = os.path.splitext(filename)
            return extension
