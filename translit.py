#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse

class Translit(object):
    """ TODO: This docstring. """
    def __init__(self, table = False, file = False):
        # Define some tables - ISO 639-1 naming convention
        self.tables = {
            'hr_en':
                {
                    u'Č': u'CH',
                    u'Ć': u'CH\'',
                    u'Ž': u'ZH',
                    u'Š': u'SH',
                    u'Đ': u'DY',
                    u'J': u'Y',
                    u'č': u'ch',
                    u'ć': u'ch\'',
                    u'ž': u'zh',
                    u'š': u'sh',
                    u'đ': u'dy',
                    u'j': u'y', # Jot palatal...
                    u'C': u'TS', # C je tkz. "ts" u izgovoru
                    u'c': u'ts'
                },
            'rs_cyr_rs_lat':
                {
                    u'А': u'A',
                    u'Б': u'B',
                    u'В': u'V',
                    u'Г': u'G',
                    u'Д': u'D',
                    u'Ђ': u'Đ',
                    u'Е': u'E',
                    u'Ж': u'Ž',
                    u'З': u'Z',
                    u'И': u'I',
                    u'Ј': u'J',
                    u'К': u'K',
                    u'Л': u'L',
                    u'Љ': u'LJ',
                    u'М': u'M',
                    u'Н': u'N',
                    u'Њ': u'NJ',
                    u'О': u'O',
                    u'П': u'P',
                    u'Р': u'R',
                    u'С': u'S',
                    u'Т': u'T',
                    u'Ћ': u'Ć',
                    u'У': u'U',
                    u'Ф': u'F',
                    u'Х': u'H',
                    u'Ц': u'C',
                    u'Ч': u'Č',
                    u'Џ': u'Dž',
                    u'Ш': u'Š',
                    u'а': u'a',
                    u'б': u'b',
                    u'в': u'v',
                    u'г': u'g',
                    u'д': u'd',
                    u'ђ': u'đ',
                    u'е': u'e',
                    u'ж': u'ž',
                    u'з': u'z',
                    u'и': u'i',
                    u'ј': u'j',
                    u'к': u'k',
                    u'л': u'l',
                    u'љ': u'lj',
                    u'м': u'm',
                    u'н': u'n',
                    u'њ': u'nj',
                    u'о': u'o',
                    u'п': u'p',
                    u'р': u'r',
                    u'с': u's',
                    u'т': u't',
                    u'ћ': u'ć',
                    u'у': u'u',
                    u'ф': u'f',
                    u'х': u'h',
                    u'ц': u'c',
                    u'ч': u'č',
                    u'џ': u'dž',
                    u'ш': u'š'
                },
            'ru_ISO9':
                {
                    u'А': u'A',
                    u'Б': u'B',
                    u'В': u'V',
                    u'Г': u'G',
                    u'Д': u'D',
                    u'Е': u'E',
                    u'Ё': u'Ë',
                    u'Ж': u'Ž',
                    u'З': u'Z',
                    u'И': u'I',
                    u'Й': u'J',
                    u'К': u'K',
                    u'Л': u'L',
                    u'М': u'M',
                    u'Н': u'N',
                    u'О': u'O',
                    u'П': u'P',
                    u'Р': u'R',
                    u'С': u'S',
                    u'Т': u'T',
                    u'У': u'U',
                    u'Ф': u'F',
                    u'Х': u'H',
                    u'Ц': u'C',
                    u'Ч': u'Č',
                    u'Ш': u'Š',
                    u'Щ': u'Ŝ',
                    u'Ъ': u'ʺ',
                    u'Ы': u'Y',
                    u'Ь': u'\'',
                    u'Э': u'È',
                    u'Ю': u'Û',
                    u'Я': u'Â',
                    # LC now
                    u'а': u'a',
                    u'б': u'b',
                    u'в': u'v',
                    u'г': u'g',
                    u'д': u'd',
                    u'е': u'e',
                    u'ё': u'ë',
                    u'ж': u'ž',
                    u'з': u'z',
                    u'и': u'i',
                    u'й': u'j',
                    u'к': u'k',
                    u'л': u'l',
                    u'м': u'm',
                    u'н': u'n',
                    u'о': u'o',
                    u'п': u'p',
                    u'р': u'r',
                    u'с': u's',
                    u'т': u't',
                    u'у': u'u',
                    u'ф': u'f',
                    u'х': u'h',
                    u'ц': u'c',
                    u'ч': u'č',
                    u'ш': u'š',
                    u'щ': u'ŝ',
                    u'ъ': u'ʺ',
                    u'ы': u'y',
                    u'ь': u'\'',
                    u'э': u'è',
                    u'ю': u'û',
                    u'я': u'â'
                },
            'be_ISO9':
                {
                    u'А': u'A',
                    u'Б': u'B',
                    u'В': u'V',
                    u'Г': u'G',
                    u'Ґ': u'G̀',
                    u'Д': u'D',
                    u'Е': u'E',
                    u'Ё': u'Ë',
                    u'Ж': u'Ž',
                    u'З': u'Z',
                    u'И': u'I',
                    u'Й': u'J',
                    u'К': u'K',
                    u'Л': u'L',
                    u'М': u'M',
                    u'Н': u'N',
                    u'О': u'O',
                    u'П': u'P',
                    u'Р': u'R',
                    u'С': u'S',
                    u'Т': u'T',
                    u'У': u'U',
                    u'Ў': u'Ǔ',
                    u'Ф': u'F',
                    u'Х': u'H',
                    u'Ц': u'C',
                    u'Ч': u'Č',
                    u'Ш': u'Š',
                    u'’': u'’',
                    u'Ы': u'Y',
                    u'Ь': u'´',
                    u'Э': u'È',
                    u'Ю': u'Û',
                    u'Я': u'Â',
                    # LC now
                    u'а': u'a',
                    u'б': u'b',
                    u'в': u'v',
                    u'г': u'g',
                    u'ґ': u'g̀',
                    u'д': u'd',
                    u'е': u'e',
                    u'ё': u'ë',
                    u'ж': u'ž',
                    u'з': u'z',
                    u'и': u'i',
                    u'й': u'j',
                    u'к': u'k',
                    u'л': u'l',
                    u'м': u'm',
                    u'н': u'n',
                    u'о': u'o',
                    u'п': u'p',
                    u'р': u'r',
                    u'с': u's',
                    u'т': u't',
                    u'у': u'u',
                    u'ў': u'ǔ',
                    u'ф': u'f',
                    u'х': u'h',
                    u'ц': u'c',
                    u'ч': u'č',
                    u'ш': u'š',
                    u'’': u'’',
                    u'ы': u'y',
                    u'ь': u'´',
                    u'э': u'è',
                    u'ю': u'û',
                    u'я': u'â'
                }
        }

    def run(self):
        # Arg parse!
        parser = argparse.ArgumentParser(description = 'Transliterates the given text either by piping it into the script itself or by point the script to the text file.\nThe data is then echoed or put in a text file.')
        parser.add_argument('-f', '--file', help='The file to read the text data from, otherwise piped data is processed.')
        parser.add_argument('-o', '--output', action='store_true', help='Output to a file. If this is not set, the data is printed (echoed)')
        parser.add_argument('table', help='Translation table used for translating. You must provide this.')

        # Parse
        args = parser.parse_args()

        # Let's make it easier for us
        self.file    = args.file
        self.output  = args.output
        self.table   = args.table

        # Do we have a source file?
        if not self.file:
            for line in sys.stdin:
                # Call the translit def here
                line = unicode(line, 'utf-8')
                self.parse(line)
                return

        # We have the file, then just read the contents and send it off to parse.
        fp = open(self.file, 'rb')
        if not fp:
            exit('Uh oh...cannot read the file: ' + self.file)

        # Try to read...
        data = fp.read()
        data = unicode(data, 'utf-8') # We need to work with UTF-8! Duh
        if not data:
            exit('Could not retrieve the data from the file!')

        fp.close()

        # Hand it over to the parser
        self.parse(data)

    def parse(self, data, return_data = False):
        # Allocate an empty var for the data
        out = ''
        out = unicode(out, 'utf-8')

        fails = 0

        # Does the supplied table exist?
        for k, v in self.tables.iteritems():
            #print k# -> hr_en, en_hr
            if k == self.table: # Got the table, do the replacement!
                #print 'Got' + k + '=' + self.table
                for r in data: # For each letter...
                    #print r
                    #if self.tables[k][r] == r:
                    if r in self.tables[k]:
                        #pass
                        #print self.tables[k][r],
                        #sys.stdout.write(self.tables[k][r])
                        out += self.tables[k][r]
                    else:
                        #pass
                        #sys.stdout.write(r)
                        out += r

                # Could have split this into 2 functions, but let's keep it short and simple.
                if return_data:
                    return out
                else:
                    sys.stdout.write(out)
                    return
                #return # Could have split this into 2 functions, but let's keep it short and simple.
            else:
                fails = fails+1
                #print k
                pass
                #print 'Not: ' + self.table
            #for a, b in self.tables[k].iteritems():
                #print a -> j (...)

        if fails == len(self.tables):
            print 'Table not found!'

if __name__ == '__main__':
    try:
        # Load the tables and initialize yourself.
        Translit = Translit()
        """
        Assuming it's used from a CLI (terminal/command prompt)
        """
        Translit.run()

    except KeyboardInterrupt:
        quit('^C received, exiting...')
