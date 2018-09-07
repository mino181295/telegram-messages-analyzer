#!/usr/bin/env python

import csv, sys, glob, time
import logging, argparse, configparser

from collections import Counter
from utils.html import TelegramAdapter as ta
from utils.html import HTMLUtility
from utils.files import FileUtility
from utils.date import DateUtility

from message import Message
from logging.config import fileConfig

# Exit codes
OK = 0
ERROR_CODE_FILENOTFOUND = 1
ERROR_CODE_HTMLPARSER = 2

RESULT_PATH = 'result'

def top_user(messages, export=False):
    logger = logging.getLogger('main')
    logger.info("Starting top user process")
    start = time.time()
    # Data analysis
    user = [message.user for message in messages]
    counter = Counter(user)
    if (export):
        data_directory = RESULT_PATH + '/top_user.csv'
        with open(data_directory, "w", encoding="utf8", newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            csv_writer.writerow(['index', 'user', 'count'])
            for index, t in enumerate(counter.most_common()):
                user, count = t
                csv_writer.writerow([index + 1, user, count])
    else:
        print("Top user:")
        for index, t in enumerate(counter.most_common()):
            user, count = t
            print('%i. %s (%i)' % (index + 1, user, count))
    elapsed = time.time() - start
    logger.info("Finished top user of the week in (%d ms)", elapsed)

def top_word(messages, ignore_words=[], export=False):
    logger = logging.getLogger('main')
    logger.info("Starting top word process:")
    start = time.time()
    # Data analysis
    counter = Counter()
    splitted_messages = [message.text.split(' ') for message in messages]
    for splitted in splitted_messages:
        counter.update(counter.update(splitted))
    for ignore_word in ignore_words:
        del counter[ignore_word]
    if (export):
        data_directory = RESULT_PATH + '/top_word.csv'
        with open(data_directory, "w", encoding="utf8", newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            csv_writer.writerow(['index', 'word', 'count'])
            for index, t in enumerate(counter.most_common()):
                word, count = t
                csv_writer.writerow([index + 1, word, count])
    else:
        print("Top words:")
        for index, t in enumerate(counter.most_common(100)):
            word, count = t
            print('%i. %s (%i)' % (index + 1, word, count))
    #End
    elapsed = time.time() - start
    logger.info("Finished top word of the week in (%d ms)", elapsed)

def top_day(messages, export=False):
    logger = logging.getLogger('main')
    logger.info("Starting top day of the week process")
    start = time.time()
    # Data analysis
    dow = [DateUtility.timestamp_to_dow(message.ts) for message in messages]
    counter = Counter(dow)
    if (export):
        data_directory = RESULT_PATH + '/top_day.csv'
        with open(data_directory, "w", encoding="utf8", newline='') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            csv_writer.writerow(['index', 'day', 'count'])
            for index, t in enumerate(counter.most_common()):
                dow, count = t
                csv_writer.writerow([index + 1, dow, count])
    else:
        print("Top days of the weeks")
        for index, t in enumerate(counter.most_common()):
            dow, count = t
            print('%i. %s (%i)' % (index + 1, dow, count))
    # End
    elapsed = time.time() - start
    logger.info("Finished top day of the week in (%d ms)", elapsed)

def all_tests(messages, ignore_words=[], export=False):
    top_user(messages, export)
    top_word(messages, ignore_words, export)
    top_day(messages, export)

def setup_result(config):
    global RESULT_PATH

    FileUtility.create_directory(config.get('DEFAULT', 'result_folder'))
    RESULT_PATH = config.get('DEFAULT', 'result_folder')

def main():
    # Arguments passed to the analysis
    parser = argparse.ArgumentParser(description='Telegram messages analyzer. Author: Matteo Minardi')
    parser.add_argument('-p','--path', help='The path of the folder', required=True)
    parser.add_argument('-e','--export', help='Flag to export', required=False, default=False)
    parser.add_argument('-t','--type', help='The type of analysis', required=False, choices=["USER", "WORD", "DOW", "*"], default="*")
    args = parser.parse_args()

    # Configuration file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('config.ini')

    # Logging setup
    fileConfig('logger.ini')
    logger = logging.getLogger('main')

    # Opening and parsing a html files from args.path
    html_filenames = glob.glob(args.path + "*.html")

    if (len(html_filenames) > 0):
        logger.info("Found %i files.", len(html_filenames))
    else:
        logger.info("No files found.")
        sys.exit(OK)

    html_dict = {}
    for html_filename in html_filenames:
        try:
            with open(html_filename, encoding="utf8") as html_file:
                html_helper = HTMLUtility(html_file)
        except FileNotFoundError:
            logger.debug("File %s not found.", args.path)
            sys.exit(ERROR_CODE_FILENOTFOUND)

        if (html_helper is None):
            logger.debug("Error while creating the HTML parser.")
            sys.exit(ERROR_CODE_HTMLPARSER)
        else :
            html_dict[html_filename] = html_helper
    
    messages = []
    error_counter = 0
    for filename, html_helper in html_dict.items():
        logger.info("Extracting messages from %s", filename)
        messages_elements = html_helper.soup.find_all(ta.MESSAGE_ELEMENT, class_=ta.MESSAGE_CLASS)
        for message_el in messages_elements:
            try:
                id = message_el.get('id').replace("message", "")
                ts = message_el.find(ta.TIMESTAMP_ELEMENT, class_=ta.TIMESTAMP_CLASS).get('title')
                ts = int(DateUtility.string_to_timestamp(ts, ta.TIMESTAMP_FORMAT))
                user = message_el.find(ta.USER_ELEMENT, class_=ta.USER_CLASS).text.strip()
                text = message_el.find(ta.TEXT_ELEMENT, class_=ta.TEXT_CLASS).text.strip()

                message = Message(id, ts, user, text)
                message.clean()

                messages.append(message)
            except Exception:
                error_counter = error_counter + 1
    logger.info("Extracted: %i", len(messages))
    logger.info("Errors: %i", error_counter)

    # Sorting the messages by ts
    messages.sort(key=lambda m: m.ts)

    # Creating a result csv file with all messages
    if (args.export):
        logger.info("Creating the result file.")
        setup_result(config)

        data_directory = RESULT_PATH + '/' + config.get('DEFAULT', 'result_filename') + ".csv"
        with open(data_directory, "w", encoding="utf8", newline='') as messages_csv:
            csv_writer = csv.writer(messages_csv, delimiter=config.get('csv', 'delimiter'))
            csv_writer.writerow(['id', 'timestamp', 'user', 'text'])
            for message in messages:
                csv_writer.writerow([message.id, message.ts, message.user, message.text])
        logger.info("Created result file.")

    # Executing the choosen test
    if (args.type == '*'):
        all_tests(messages, config.get('data', 'ignore').split(','), args.export)
    else:
        if (args.type == 'WORD'):   
            top_word(messages, config.get('data', 'ignore').split(','), args.export)
        elif (args.type == 'USER'): 
            top_user(messages, args.export)
        elif (args.type == 'DOW'):  
            top_day(messages, args.export)

    sys.exit(OK)

if __name__ == "__main__":
    main()
