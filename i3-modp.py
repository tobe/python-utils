#!/usr/bin/env python
# -*- coding: utf-8 -*-
# i3-modp 1.0

import subprocess
from subprocess import Popen, PIPE

try:
    import i3ipc
except ImportError:
    print('i3-modp cannot work without i3ipc. Exiting...')
    exit()

def show_menu(data, lines):
    dmenu_input = bytes(str.join('\n', data), 'UTF-8')
    dmenu_args  = ['dmenu'] + ['-b','-i'] # Change this to make it more appealing!
    dmenu_cmd = dmenu_args + ['-l', str(lines)]

    p = Popen(dmenu_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(dmenu_input)
    return stdout

def main():
    conn = i3ipc.Connection()
    outputs = conn.get_tree().leaves()

    windows = []
    for a in outputs:
        windows.append(a.name)

    # Receive the command
    cmd = show_menu(windows, len(windows)).decode('UTF-8').strip()

    # Execute the command
    conn.command('[title="%s"] focus' % cmd)

if __name__ == '__main__':
    main()
