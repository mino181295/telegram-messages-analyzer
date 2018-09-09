import os
import zipfile

class FileUtility(object):
 
    @staticmethod
    def is_zipfile(path):
        return zipfile.is_zipfile(path)

    @staticmethod
    def is_directory(path):
        return os.path.exists(path) and os.path.isdir(path)

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
