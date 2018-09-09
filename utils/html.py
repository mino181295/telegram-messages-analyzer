from bs4 import BeautifulSoup

class HTMLUtility(object):

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

class TelegramAdapter(object):

    MESSAGE_SELECTOR = ".message.default.clearfix" 
    MESSAGE_JOINED_CLASS = "joined" 

    TIMESTAMP_ELEMENT = "div" 
    TIMESTAMP_CLASS = "pull_right date details" 
    TIMESTAMP_FORMAT = "%d.%m.%Y %H:%M:%S" 

    USER_ELEMENT = "div" 
    USER_CLASS = "from_name" 

    TEXT_ELEMENT = "div" 
    TEXT_CLASS = "text" 

    
    
    