#!/usr/bin/python
import sys, urllib2
import re

def main():
    if len(sys.argv) < 2:
        exit('Not enough arguments. Need a champion name.');

    champion = sys.argv[1].strip().lower().replace(' ','') # Get the name, strip spaces and strtolower it.

    # Got the champion, now do the request.
    try:
        data = urllib2.urlopen('http://www.lolcounter.com/champ/' + champion).read()
    except urllib2.HTTPError, e:
        exit('HTTP Error: %s. Request failed.' % e.code)
    except:
        exit('Fatal exception.')

    # regex
    regex = re.findall("([a-zA-Z]*)\s*<div class=\"pull-right champ-like-bar\">\s*<div class=\"progress progress-success\"><div class=\"bar\" style=\"width:([0-9]{0,3})", data, re.IGNORECASE)
    if not regex or (regex == None):
        exit('Regular expression failed.')

    i = 0
    for champ, hardness in regex:
        if i == 0:
            print '=== Bad against ==='
        elif i == 5:
            print '\n\n === Good against ==='
        elif i == 10:
            print '\n\n === Good with ==='
        elif i == 15:
            exit()

        print '* ' + champ.strip() + '\t [' + hardness + '%]'
        i = i+1

    #print regex

    # regex

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('^C caught, exiting...')
