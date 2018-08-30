import os

class FileUtility(object):
 
    @staticmethod
    def file_extension(filename):
        if '.' in filename:
            _, extension = os.path.splitext(filename)
            return extension

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
