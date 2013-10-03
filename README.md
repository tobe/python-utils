##python-utils
These are really simple utilities I made either just for fun or for some really light usage.
if there is no documentation for every single file, hey, you'll just have to find your way around ;-)

###irssi-config.py
`irssi-config.json` is used with this project.
irssi-config.py generates a config file for irssi (`config`).


The configuration is specified in the .json file. You can use the one provided as an example.
The concept is really simple to get around, just use your brain and your javascript object notation sense.



Here's more specific stuff:
`"ssl": 1` under `"Servers"` has three options that correspond on how irssi handles encryption:

`"ssl": 0` will trigger `"use_ssl": "no"`. 

`"ssl": 1` will trigger the usage of ssl to: `"use_ssl": "yes"` but it WILL set `"ssl_verify"` to `"no"`. 

`"ssl": 2` will act as the upper ^ option and it will set `"ssl_verify"` to `"yes"`. This is also the "paranoid" option. 


You should probably change `count_start` on line ~7 so the script knows from where on to start counting your WINDOWS.
This is because some people (including myself), use hilight and root windows which are set to 1 and 2. The rest are channels.


In "real world", you should use this application by piping the return to a file using a command line interpreter, so for example...
`/cygdrive/c/Python27/python-utils $ python irssi-config.py > config`

would echo it out to `./config`. Then you can use `scp` or such to transfer it, or alternatively you could run the script itself on the shell server.


####Notes
The WINDOWS generated are presumed to be IRC and their tags match the corresponding chatnets.
Hilights are set to both text, nick AND word. You can change these later on.
Maximum kicks are set to 100, msgs 100 and a single whois (Who even needs this? I dislike this). You can, of course change all of these once the config is generated.
