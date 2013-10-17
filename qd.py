#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import urllib2
import urlparse
import socket
import time
import sys
import datetime

""" Taken from php2python.com """
def date(unixtime, format = '%d.%m.%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

""" Taken from http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size """
def filesize(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.3f %s" % (num, x)
        num /= 1024.0
    return "%3.3f%s" % (num, 'TB')

def main():
    # Define some arguments
    parser = argparse.ArgumentParser(description='Downloads a file off WAN. Supports only raw HTTP protocol. Dynamically adjusts the buffer size so the download is as fast as possible.')
    parser.add_argument('--chunk', type=int, default=8192, help='Manually enter the buffer size (chunk size). This tends to be automatically adjusted.')
    parser.add_argument('--quiet', action='store_true', help='Output nothing.')
    parser.add_argument('url')

    # Parse the arguments
    args = parser.parse_args()

    chunk = args.chunk
    quiet = args.quiet
    url   = args.url

    if not url:
        quit('Cannot continue without a URL.')
        sys.stdout.flush()
        if not quiet:
            print '[+] Got the URL argument...'
            sys.stdout.flush()

    # We got the URL as an argument...now check whether urlopen can actually /load/ it.
    try:
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1587.0 Safari/537.36',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en',
                'Connection': 'keep-alive',
                'Encoding': 'gzip,deflate,sdch',
        }

        request = urllib2.Request(url, None, headers)
        handle = urllib2.urlopen(request)
    except (urllib2.URLError, urllib2.HTTPError) as e:
        quit('[-] Failed to load the URL, got exception ' + str(e.reason) + '. Cannot continue, exiting...')
        sys.stdout.flush()

    # Install urllib2 properly, to handle cookies
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor()))
    socket.setdefaulttimeout(120) # Set the timeout to two minutes.

    # The URL is loaded at this point, get some information about the server, standard stuff, reda radi.
    print '[+] The URL is ' + handle.geturl()
    sys.stdout.flush()
    print '[+] Got HTTP ' + str(handle.getcode())
    sys.stdout.flush()
    if handle.getcode() == 200:
        print '[+] 200 OK ;-)'
        sys.stdout.flush()
    else:
        print '[-] HTTP is NOT OK :S' # Man, that sucks
        sys.stdout.flush()
    print '[+] Printing HTTP response headers...\n'
    sys.stdout.flush()

    x = dict(handle.info())
    for k, v in x.iteritems():
        print '[+] %s: %s' % (k, v)
        sys.stdout.flush()

    # Now resolve some internet protocol addresses!
    ip = socket.gethostbyname(urlparse.urlparse(handle.geturl()).netloc)
    print '\n[+] IP: ' + socket.gethostbyname(urlparse.urlparse(handle.geturl()).netloc)
    sys.stdout.flush()
    # And now get the hostname from the IP...
    print '[+] Hostname: ' + str(socket.gethostbyaddr(ip)[0])
    sys.stdout.flush()
    # The most important part now...how big is the file?
    print '[+] File size is ' + filesize(int(handle.info()['Content-Length']))
    sys.stdout.flush()

    # Get the newly created file name by splitting the URL and taking the last part in the flowing directory.
    file_name = url.split('/')[-1]
    try:
        fp = open(file_name, 'wb') # Write binary
    except IOError as e:
        quit('[-] Failed to create a temporary file. Permissions? $ chmod. Cannot continue.')
        sys.stdout.flush()
    print '[+] Partial file created, write permissions are available.'
    sys.stdout.flush()

    # Determine the divider usign the file bytes.
    if not int(handle.info()['Content-Length']):
        print '[-] Unable to automatically determine the chunk size. Using the --chunk'
        sys.stdout.flush()
        if chunk == 8192:
            print '[+] Chunk size set to default (8192)'
            sys.stdout.flush()

    bytes = int(handle.info()['Content-Length'])
    if 0 <= bytes <= 1024:
        divider = 1
    elif 1024 <= bytes <= 10485760:
        divider = 10
    elif 10485760 <= bytes <= 104857600:
        divider = 10
    elif 104857600 <= bytes <= 1048576000:
        divider = 100
    elif 1048576000 <= bytes <= 10485760000:
        divider = 1000

    a = bytes/divider
    chunk_size = int(round(a/1024)) # Kilobytes
    print '[+] Chunk size automatically set to ' + str(chunk_size)
    sys.stdout.flush()

    print '[+] Download is ready to start. Press Enter to start.'
    sys.stdout.flush()
    raw_input('')
    sys.stdout.flush()
    time.sleep(1)

    # Everything looks OK, download should start
    dl_so_far  = 0
    start_time = time.time() # UNIX timestamp equal to php time();
    i          = 0
    print '[+] Download started @ ' + date(start_time)
    sys.stdout.flush()
    try:
        while True:
            sys.stdout.flush()
            block        = handle.read(chunk_size) # Read into `block`
            dl_so_far   += len(block)

            if len(block) >= bytes or len(block) == 0: # Download finished.
                break # Exit out of loop
            fp.write(block) # Write it to a file.

            i = i+1

            percent = float(dl_so_far) / bytes
            percent = round(percent*100, 2)

            time_passed = time.time() - start_time
            already_loaded = float(i*chunk_size)
            speed = already_loaded/1048576
            speed = speed / time_passed

            print '[%.2f%%][#%s] Downloaded %s of %s\t\t\t%.3f MB/s' % (percent, str(i), str(filesize(dl_so_far)), str(filesize(bytes)), speed)
            sys.stdout.flush()
    except socket.timeout:
        quit('[-] Connection timed out. Aborted.')

    print '[+] Finished @'
    sys.stdout.flush()
    print '[+] Download took '
    sys.stdout.flush()

    # Don't forget to os.rename(file_name + '.part', file_name)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit('^C received, exiting...')
