#!/usr/bin/python
import os
import json

def run():
    # Start counting channels from 3...because of hilight and (ALL).
    count_start = 3

    # Is there .json there?
    if not os.path.exists('./irssi-config.json'):
        exit('Cannot continue without a .json file. Exiting...')

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
    # ::: SERVER INFO :::
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

    # End server info & start the chatnets.
    output += '\n);\n'
    output += 'chatnets = {\n'

    # ::: CHATNETS :::
#    i = 1
    for chatnets in data['Chatnets']:
        # Autosend blank?
        if not 'autosend' in chatnets:
            chatnets['autosend'] = 'echo \'What are you looking for here?\''

        output += '\t' + chatnets['name'] + ' = ' + '{\n'
        output += '\t\ttype = "' + chatnets['type'] + '";\n'
        output += '\t\tautosendcmd = "' + chatnets['autosend'] + '";\n'
        output += '\t\tmax_kicks = "100";\n'
        output += '\t\tmax_msgs = "100";\n'
        output += '\t\tmax_whois = "1";\n'
        output += '\t};\n'

    # Start the channels.
    output += 'channels = (\n'

    # ::: CHANNELS :::
    i = 1
    for channels in data['Channels']:
        output += '\t{\n'
        output += '\t\tname = "' + channels['name'] + '";\n'
        output += '\t\tchatnet = "' + channels['chatnet'] + '";\n'
        output += '\t\tautojoin = "yes";\n'

        if i == len(data['Channels']):
            output += '\t}'
        else:
            output += '\t},\n'
        i = i + 1

    # End the channels and start with Hilights
    output += '\n);\n'

    # Poof, show the user to paste their own stuff here.
    output += '\n### PASTE YOUR OWN ALIASES HERE ###\n\n\n\n\n\n'
    output += '### PASTE YOUR OWN STATUSBAR HERE ###\n\n\n\n\n\n'
    output += '### PASTE YOUR OWN SETTINGS HERE ###\n\n\n\n\n\n'

    output += 'hilights = (\n'

    # ::: HILIGHTS :::
    i = 1
    for hilights in data['Hilights']:
        output += '\t{\n'
        output += '\t\ttext = "' + hilights['text'] + '";\n'
        output += '\t\tnick = "' + hilights['nick'] + '";\n'
        output += '\t\tword = "' + hilights['word'] + '";\n'

        if i == len(data['Hilights']):
            output += '\t}'
        else:
            output += '\t},\n'
        i = i + 1

    # And we're done...now off to windows and we're done!
    output += '\n);\n'


    # ::: WINDOWS :::
    # Start counting from window number count_start
    # strstr()
    output += 'windows = {\n'

    for windows in data['Channels']:
        output += '\t' + str(count_start) + ' = {\n'
        output += '\t\titems = (\n'
        output += '\t\t\t{\n'
        output += '\t\t\t\ttype = "CHANNEL";\n'
        output += '\t\t\t\tchat_type = "IRC";\n'
        output += '\t\t\t\tname = "#' + windows['name'] + '";\n'
        output += '\t\t\t\ttag = "' + windows['chatnet'] + '";\n'
        output += '\t\t\t}\n'
        output += '\t\t);\n'
        output += '\t};\n\n'
        count_start = count_start + 1

    output += '### PASTE YOUR mainwindows AND SUCH HERE ### THE END / FIN / KRAJ / KONEC ###\n\n\n'
    output += '};\n\n\n'

    # User should pipe this out into a file with >.
    print output

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        exit('^C received, exiting...');
