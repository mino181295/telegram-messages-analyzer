#!/usr/bin/env python

import sys
import glob
import argparse

from utils.html import TelegramHTMLAdapter as ta
from utils.html import HTMLUtility
from utils.files import FileUtility

from message import Message

# Error codes
ERROR_CODE_FILENOTFOUND = 1
ERROR_CODE_HTMLPARSER = 2

def get_html_filenames_from_folder(folder_name, file_extension="html"):
    return glob.glob(folder_name + "*" + file_extension)

def get_message(id, ts, user, text):
    return 

def main():
    # Arguments passed to the analysis
    parser = argparse.ArgumentParser(description='Telegram messages analyzer. Author: Matteo Minardi')
    parser.add_argument('-p','--path', help='The path of the folder', required=True)
    parser.add_argument('-t','--type', help='The type of analysis', required=False, choices=["USER", "WORD", "DOW", "*"], default="*")
    
    args = parser.parse_args()

    # Opening and parsing a html files from args.path
    html_dict = {}
    html_filenames = get_html_filenames_from_folder(args.path)
    for html_filename in html_filenames:
        try:
            with open(html_filename, encoding="utf8") as html_file:
                html_helper = HTMLUtility(html_file)
        except FileNotFoundError:
            print("File " + args.path + " not found.")
            sys.exit(ERROR_CODE_FILENOTFOUND)

        if (html_helper is None):
            print("Error while creating the HTML parser.")
            sys.exit(ERROR_CODE_HTMLPARSER)
        else :
            html_dict[html_filename] = html_helper
    print("Found", len(html_dict), "files.")

    messages = []
    for filename, html_helper in html_dict.items():
        print("Parsing " + filename + "..")
        messages_elements = html_helper.soup.findAll(ta.MESSAGE_ELEMENT, { "class": ta.MESSAGE_CLASS.split(" ") })
        
        for message_el in messages_elements:
            id = message_el.get('id')
            ts = message_el.find('div', { "class": "pull_right date details".split(" ")}).get('title')
            
            user_el= message_el.find('div', { "class": "from_name"})
            user = None if user_el is None else user_el.text

            text_el= message_el.find('div', { "class": "text"})
            txt = None if text_el is None else text_el.text

            if not ((id is None) or (ts is None) or (user is None) or (txt is None)):
                messages.append(Message(id, ts, user, txt))

        print("Extracted", len(messages), "plain messages.")

    sys.exit(0)

if __name__ == "__main__":
    main()
