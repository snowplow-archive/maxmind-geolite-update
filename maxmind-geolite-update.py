#!/usr/bin/env python

"""maxmind-geolite-update: Updates the MaxMind geo IP databases"""

# Standard command-line imports
import os, sys, optparse
import ConfigParser
import datetime
import urllib2
import zipfile

__author__ = "Alex Dean"
__copyright__ = "Copyright 2012, Psychic Bazaar Ltd"
__status__ = "Production"
__version__ = "0.1"

# Get the default configuration file for this script
CONFIG_FILE = os.path.dirname( os.path.realpath( __file__ ) ) + "/config.cfg"

def controller():
    """Runs program and handles command line options"""

    parser = optparse.OptionParser(description='Updates the free MaxMind geo databases',
                                   prog='maxmind-geolite-update',
                                   version='maxmind-geolite-update' + __version__)
    parser.add_option('--config', '-c',
                      help='config file. Default is ' + CONFIG_FILE,
                      dest='config',
                      default=CONFIG_FILE)

    # Now parse the args
    (opts, args) = parser.parse_args()

    # Load the configuration file
    config = ConfigParser.ConfigParser()
    config.read(opts.config)

    # User-configurable vars
    download_dir = config.get('Local', 'download-dir')
    destination_dir = config.get('Local', 'destination-dir')

    # MaxMind-specific vars 
    maxmind_uri = config.get('MaxMind', 'uri')

    # MaxMind:local file mappings
    maxmind_files = config._sections['Files']
    del maxmind_files['__name__']

    # Check directories exist
    if not os.path.isdir(download_dir):
        raise Exception("Download directory %s does not exist" % download_dir)
    if not os.path.isdir(destination_dir):
        raise Exception("Destination directory %s does not exist" % destination_dir)

    # Iterate through the files and download as necessary
    for local, remote in maxmind_files.iteritems():
        return_code = mirror(maxmind_uri + remote, os.path.join(download_dir, local))
        if (return_code >= 200 and return_code < 400) and return_code != 304:

            # Generate the unzipped filename
            unzipped_file = os.path.splitext(local)[0] 

            # Unzip the file 
            zf = zipfile.ZipFile(local)
            zf.extract(unzipped_file, destination_dir) 

            # Created notification message and print
            notification = "Updated MaxMind database file %s" % (destination_dir + "/" + unzipped_file)
            print notification

            # Notify HipChat of the update, if we have an account
            # TODO

def mirror(uri, file):
    """Crude approximation of Perl's awesome mirror() function using urllib2"""

    # Start building the request
    req = urllib2.Request(uri)

    # Add the file's datestamp as the If-Modified-Since, if it exists
    if os.path.isfile(file):
        last_modified = os.path.getmtime(file)
        req.add_header("If-Modified-Since", datetime.datetime.fromtimestamp(last_modified))

    # Add the user-agent
    req.add_header("User-agent", "maxmind-geolite-update/" + __version__)
 
    opener = urllib2.build_opener(NotModifiedHandler())
    resp = opener.open(req)
    headers = resp.info()

    # Write the file if we need to
    if (resp.code >= 200 and resp.code < 400) and resp.code != 304:
        local_file = open(file, 'w')
        local_file.write(resp.read())
        local_file.close()

    return resp.code

# class HipChatLogger():


class NotModifiedHandler(urllib2.BaseHandler):
    """Taken from http://www.artima.com/forums/flat.jsp?forum=122&thread=15024"""
 
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl

if __name__ == '__main__':
    controller()
