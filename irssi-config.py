#!/usr/bin/python
import os
import json

def run():
    # Start counting channels from 3...because of hilight and (ALL).
    count_start = 3

    # Is there .json there?
    if not os.path.exists('./irssi-config.json'):
        exit('Cannot continue without an .ini file. Exiting...')

    # Parse the JSON, check if it's valid
    try:
        data = json.load(open('./irssi-config.json', 'rb'))
    except ValueError, e:
        exit('Something has gone wrong in irssi-config.json, cannot parse the json!\n' + str(e))

    # Reserve a blank string for concatination purposes later on
    output = ''

    # Let's begin.
    output += 'servers = ('

    # Parse the json file
    # ssl: 0 = off, 1 = on, 2 = paranoid
    # Parse auto: max_kicks = "100"; max_msgs = "100"; max_whois = "1";
    # All channels have autojoin = "yes"
    #    recode_fallback = "utf-8"; settings_autosave = "yes"; -> automatic

    #print data
    #print len(data['Servers'])
    #exit()

    i = 1
    for s_info in data['Servers']: # Foreach server info
        #print s_info['name']
        output += '\n\t{\n'
        output += '\t\tchatnet = "' + s_info['name'] + '";\n'
        output += '\t\taddress = "' + s_info['address'] + '";\n'
        output += '\t\tport = "' + str(s_info['port']) + '";\n'

        # Check for SSL paranoidness
        if s_info['ssl'] == 2:
            output += '\t\tuse_ssl = "yes";\n'
            output += '\t\tssl_verify = "yes";\n'
        elif s_info['ssl'] == 1:
            output += '\t\tuse_ssl = "yes";\n'
            output += '\t\tssl_verify = "no";\n'
        else:
            output += '\t\tuse_ssl = "no";\n'

        output += '\t\tautoconnect = "' + s_info['autoconnect'] + '";\n'

        if i == len(data['Servers']):
            output += '\t}'
        else:
            output += '\t},'
        i = i + 1


    print output

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        exit('^C received, exiting...');