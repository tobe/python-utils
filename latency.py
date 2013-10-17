import sys
import argparse
import time
import socket

def run():
    # Invoke the argument parser and add some core arguments.
    parser = argparse.ArgumentParser(description='"Pings" the given host in order to determine latency between requests.')
    parser.add_argument('-host', help='The host, can be in both IPv4 form and in the hostname form.')
    parser.add_argument('-port', type=int, default=80, help='The port, by default it\'s 80. Any other port can be specified by using this parameter.')
    parser.add_argument('-protocol', default='TCP', choices=['TCP', 'UDP'], help='The protocol used for the socket. This can be either TCP or UDP, SOCK_STREAM for TCP and SOCK_DGRAM for UDP based sockets.')
    parser.add_argument('-c', '--count', type=int, default=4, help='Numbers of times to "ping" the host. By default this is 4.')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Time before the request times out. By default this is 10.')
    parser.add_argument('-nostop', help='Don\'t stop!', action='store_true')
    # Parse the arguments...
    args = parser.parse_args()

    # Define some variables, just to make it easier.
    host     = args.host
    port     = args.port
    protocol = args.protocol
    count    = args.count
    timeout  = args.timeout
    nostop   = args.nostop

    # Host and port are _required_
    if not host or not port:
        exit('Expected a host and a port.\nPlease refer to the usage by doing $ ' + sys.argv[0] + ' -h')

    # Validate the host...
    try:
        socket.gethostbyname(host)
    except socket.error:
        # Failed to resolve the hostname...perhaps it's an IP after all.
        try:
            socket.inet_aton(host)
        except socket.error:
            # We really fail now, time to terminate.
            exit('Failed to validate the host. Both the IP validation and the host validation failed. Are you sure the host exists?')

    # Let the magic begin!
    print 'Connecting to host %s via %s, %d times.\n' % (host, protocol, count)

    # Determine how many times we actually connect...
    highest = 0
    lowest = 0
    i = 0
    loss = 0
    total = 0

    # Nostop flag?
    if nostop:
        count = 65535

    while i < count:
        try:
            if protocol == 'TCP':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # It's a TCP socket...
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # It's a UDP socket...CS 1.6 time.

            # Set the timeout...
            sock.settimeout(timeout)

            now = time.time()
            sock.connect((host, port)) # Connect!
            then = time.time()

            sock.shutdown(socket.SHUT_RDWR)
            sock.close() # Remember to close the connection so the other socket can proceed.

            diff = (then - now)
            diff = int(diff * 1000) # Convert UNIX difference to miliseconds.

            # Add up to total.
            total = total + diff

            # HIGHEST round trip determination:
            if diff > highest:
                highest = diff

            # LOWEST round trip determination:
            if lowest == 0:
                lowest = diff
            if diff < lowest:
                lowest = diff

            # Print it out ;-)
            print '%s: seq=%d time=%d ms' % (host, i, diff)

        except timeout: # Not sure whether this works or not...
            loss = loss + 1
            print '%s: seq=%d time=timeout' % (host, i)

        except socket.error as er:
            print 'An error has occured! Error: %s' % (er)
            exit()
        i = i + 1
        # FLUSH the output
        sys.stdout.flush()
        # TAKE A BREAK, for a second.
        time.sleep(1)

    # Statistics
    print '\n--- Statistics for %s ---' % (host)
    sc = i - loss # Successfull connections = Number of times - loss.
    print '%d successful connections made, %d timed out (dropped)' % (sc, loss)

    # Aritmetichka sredina...average calculation = total / times connected
    average = (total / i)
    print 'round trip (ms): min/avg/max = %d/%d/%d' % (lowest, average, highest)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt, e:
        print '^C received, exiting...'
        exit('^C received, exiting...')
