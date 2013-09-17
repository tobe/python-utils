#!/usr/bin/python

def run():
    l = [0]*256 # Empty workload
    # Start at address (key) 0
    pos = 0
    data = '++++++++++++++++>>>>>>>>>>++>>--<<<<<<++++++++'; # hm

    # Perform a switch here so we know what's up
    for char in data:
        if char == '+':
            # Zbroji
            l[pos] = l[pos] + 1
        elif char == '-':
            # Oduzmi
            l[pos] = l[pos] - 1
        elif char == '>':
            # Pomak u desno
            pos = pos + 1
        elif char == '<':
            # Pomak u lijevo
            pos = pos - 1

    print l

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        exit('0')