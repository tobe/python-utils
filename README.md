**THE README IS MUCH MORE READABLE BY CLICKING [HERE](https://github.com/infyhr/python-utils/blob/master/README.md)**

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

###geolocation.py
Spoof your current location with this. Designed to work with firefox. Works under Windows (Cygwin32+W8 Pro x64) and Linux.
You can use this with Chrome as well, but I can image it's a little bit harder to tweak the browser to use a third party geolocation server. By default firefox uses Google's geolocation API, as well.


The whole thing has been hacked in under 5 minutes. I was curious enough about it and since I've been spoofing my android geolocation via "Mock Locations" and a shorthand MITM, I thought I could do something similar here.
Follow these steps in order to configure the program itself:

1. Open Firefox, navigate to `about:config` and create a new string called `geo.wifi.uri`. Set its value to `http://localhost:1950/`. Alternatively, you can change the port and the IP to your likings, but we'll keep it simple for now. Don't forget the `http://` prefix.
2. Open `geolocation.py` and edit the following values on lines ~9~11 to your likings: `latitude`, `longtitude` and `accuracy`. You can use Google Maps or some other service in order to find these, just google. Don't forget these *MUST* be strings!
3. Navigate to the bottom of the file on line ~29, and if you wish change the IP address if you are running multiple NICs and/or the port. But [you should love 1950](http://en.wikipedia.org/wiki/Torcida_Split).
4. Run the script, it servers forever, so it acts like a daemon.
5. Test it over here: [http://html5demos.com/geo](http://html5demos.com/geo) (or wherever you like).
6. When the websites returns your location you can kill the server via ^C, alternatively you can keep it running so you can do more requests later on.
7. Did it work? If it did, you should've landed in Chernobyl by default. If not, you did something wrong.

If you would like to learn more about Google's geolocation and how I got the response, click [here](https://developers.google.com/maps/documentation/business/geolocation/#responses).
[Your cellphone works the same way](https://developers.google.com/maps/documentation/business/geolocation/#sample-requests), except it even sends cell data + the wifi networks. If you have GPS turned out, it prioritizes GPS over Geolocation.
