#!/usr/bin/env python

import argparse

from utils.utils import *

def main():
    # Arguments passed to the analysis
    parser = argparse.ArgumentParser(description='Telegram messages analyzer. Author: Matteo Minardi')
    parser.add_argument('-p','--path', help='The path of the folder', required=True)
    parser.add_argument('-t','--type', help='The type of analysis', required=False, choices=["USER", "WORD", "DOW", "*"], default="*")
    
    args = parser.parse_args()
    
if __name__ == "__main__":
    main()
