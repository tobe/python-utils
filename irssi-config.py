#!/usr/bin/python
import os

def run():
    # First let's see if the .ini is there.
    if not os.path.exists('./irssi-config.ini'):
        exit('Cannot continue without an .ini file. Exiting...')

    # Parse the json file
    # ssl: 0 = off, 1 = on, 2 = paranoid
    # Parse auto: max_kicks = "100"; max_msgs = "100"; max_whois = "1";
    # All channels have autojoin = "yes"
    #    recode_fallback = "utf-8"; settings_autosave = "yes"; -> automatic


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        exit('^C received, exiting...');