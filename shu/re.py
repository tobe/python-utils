#!/usr/bin/python
import sys
import argparse
import re

def run():
    # Set up argparse
    parser = argparse.ArgumentParser(description='Performs a python regular expression search using the re module.')
    parser.add_argument('regex', help='The regular expression itself.')
    args = parser.parse_args()

    regex = args.regex

    # For each line, perform a regex search
    i = 0
    for line in sys.stdin:
        match = re.match(regex, str(line), re.IGNORECASE | re.UNICODE)
        if match:
            print '%d. %s' % (i, match.group())
        else:
            #print 'null'
            pass
        i = i+1


if __name__ == '__main__':
    run()