#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys # Ovo nam je potrebno zbog korište?a sys.argv
import httplib # httplib > urllib2 za HTTP requeste tipa $_POST ili $_GET ;) a i PUT i DELETE.
import urllib # potreban za urlencode() ekvivalent u PHP-u.
import re # regex, potreban za traženje definicija i što ne
import HTMLParser # za pretvaranje HTML entitya tipa UTF-8 znakova vrijednosti &#x005B; u sirov znak.


def main():

    if len(sys.argv) < 2:
        raise Exception('Ne mogu nastaviti bez riječi, argumenta!')

    rije4 = sys.argv[1]
    rije4 = urllib.quote_plus(rije4) # urlencode, pretvara " " ( \0x20 ) u %20 i slično.
    print 'Pretražujem bazu HJP-a za riječ "' + rije4 + '"...'

    headers = { # Zaglav?a, tek tako zbog autentičnosti.
        "Host": "hjp.novi-liber.hr",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
        "Content-Type": "application/x-www-form-urlencoded", # Ovo...uvik mora bit tu -_-
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "__utma=13579758.1009366654.1382037497.1382037497.1382037497.1; __utmb=13579758.19.10.1382037497; __utmc=13579758; __utmz=13579758.1382037497.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
        "Referer": "http://hjp.novi-liber.hr/index.php?show=search"
    }

    # Konstrukcija varijable u kojoj se nalaze podatci potrebni za POSTa?e.
    ss = 'word=%s&search=+&osnovni_podaci=on&definicija=on&postano=true' % (rije4)

    # To je to?
    conn = httplib.HTTPConnection('hjp.novi-liber.hr')
    #conn.set_debuglevel(1)    
    conn.request('POST', 'http://hjp.novi-liber.hr/index.php?show=search', ss, headers)
    response = conn.getresponse()

    #print(response.status, response.reason)
    print 'HTTP Status: %d' % (response.status)
    print 'HTTP Reason: %s' % (response.reason)
    if response.status != 200:
        raise Exception('Nešto je pošlo po zlu...HTTP 200 nije zaprimljen, uh oh.')

    data = response.read()
    conn.close()

    # Pronađi riječ (definiciju), postoji server side correction koji ispravlja č u ć i obratno, te ije u je i obratno.
    m = re.findall('<td id="osnovni_podaci_frame">\s*<br><b>(.*)</b>', data, re.I|re.M)

    if not m[0]:
        raise Exception('Regex pojma nije pronašao niti jednu riječ...?')

    h = HTMLParser.HTMLParser()
    rije4_p = h.unescape(m[0])
    print 'Pronađena riječ:' + rije4_p.encode('utf-8')

    # A sada se pozabavi definicijom....
    m = set(re.findall('<b>([0-9]{0,1}). </b></td><td>(.*?)</td></tr>', data, re.I|re.M|re.S))
    if not m:
        raise Exception('Regex defincije nije prošao...ne postoji?')

    print 'Definicije: '

    for k, v in m:
        # Eliminiraj HTML tagove
        v = re.sub(r'<[^>]*?>', '', v)
        # Pretvori ih u "normalne" vrijednosti
        v = h.unescape(v)
        print '- %s' % (v)

    #print(data)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit('^C received, exiting...')
    except Exception, e:
        quit(e)
