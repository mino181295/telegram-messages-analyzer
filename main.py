#!/usr/bin/env python

import csv
import sys
import glob
import argparse
import configparser

from utils.html import TelegramAdapter as ta
from utils.html import HTMLUtility
from utils.files import FileUtility
from utils.date import DateUtility

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

    # Configuration file
    config = configparser.ConfigParser(allow_no_value=True)
    config.readfp(open('config.props'))

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
        print("Extracting messages from " + filename + "..")
        messages_elements = html_helper.soup.find_all(ta.MESSAGE_ELEMENT, class_=ta.MESSAGE_CLASS)
        for message_el in messages_elements:
            try:
                id = message_el.get('id').replace("message", "")
                ts = message_el.find(ta.TIMESTAMP_ELEMENT, class_=ta.TIMESTAMP_CLASS).get('title')
                ts = int(DateUtility.string_to_timestamp(ts, ta.TIMESTAMP_FORMAT))
                user = message_el.find(ta.USER_ELEMENT, class_=ta.USER_CLASS).text.strip()
                text = message_el.find(ta.TEXT_ELEMENT, class_=ta.TEXT_CLASS).text.strip()

                messages.append(Message(id, ts, user, text))
            except Exception:
                pass
    print("Extracted", len(messages), "plain messages.")

    # Sorting the messages by ts
    messages.sort(key=lambda m: m.ts)
    print("Sorted", len(messages), " messages.")

    # Creating a result csv file with all messages
    print("Creating the result file..")
    FileUtility.create_directory(config.get('DEFAULT', 'result_folder'))
    directory_path = config.get('DEFAULT', 'result_folder') + '/' + config.get('DEFAULT', 'result_filename')
    
    with open(directory_path + ".csv", "w", encoding="utf8") as messages_csv:
        csv_writer = csv.writer(messages_csv, delimiter=config.get('csv', 'delimiter'))
        csv_writer.writerow(['id', 'timestamp', 'user', 'text'])
        for message in messages:
            csv_writer.writerow([message.id, message.ts, message.user, message.text])
    print("Created result file.")

    
    sys.exit(0)

if __name__ == "__main__":
    main()
