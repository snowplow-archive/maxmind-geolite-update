# maxmind-geolite-update

## Overview

A Python script to regularly update the free MaxMind geo databases. Closely based on Boris from MaxMind's [Perl script] [perlscript] to accomplish the same.

## Installing

Grab the whole repo:

    git clone git@github.com:psychicbazaar/maxmind-geolite-update.git

By default maxmind-geolite-update reads the `nosub.cfg` configuration file. Update its contents as required:

    [Local]
    download-dir: /usr/local/share/GeoIP/download
    destination-dir: /usr/local/share/GeoIP 

If you subscribe to the commercial MaxMind GeoIP Country database and/or GeoIPCity database, then make sure to comment out the first two lines in the `[Files]` section, to avoid clashing with MaxMind's `ipupdate` tool:

    [Files]
    ; GeoIP.dat.gz: GeoLiteCountry/GeoIP.dat.gz ; DELETE this line if you are a subscriber
    ; GeoIPCity.dat.gz: GeoLiteCity.dat.gz ; DELETE this line if you are a subscriber.

If you want to change the path for the configuration file, you can specify this on the command line like so:

    ./maxmind-geolite-update.py --config=~/maxmind.cfg

[perlscript]: http://forum.maxmind.com/viewtopic.php?f=13&t=1453

## License

Copyright (C) 2012 Psychic Bazaar Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
