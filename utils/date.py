from datetime import datetime as dt

class DateUtility(object):
 
    @staticmethod
    def string_to_timestamp(string, format):
        return dt.strptime(string, format).timestamp()

    @staticmethod
    def timestamp_to_string(timestamp, format):
        ts = dt.fromtimestamp(timestamp)
        return ts.strftime(format)