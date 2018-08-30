from bs4 import BeautifulSoup

class HTMLUtility(object):

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

class TelegramHTMLAdapter(object):

    MESSAGE_ELEMENT = "div" 
    MESSAGE_CLASS = "message default clearfix" 

    
    
    