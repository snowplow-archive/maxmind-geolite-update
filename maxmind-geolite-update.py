#!/usr/bin/env python

"""maxmind-geolite-update: Updates the MaxMind geo IP databases"""

# Standard command-line imports
import os, sys, optparse
import ConfigParser
import datetime
import urllib2
import gzip

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
    download_dir = config.get('Local', 'download-dir')
    destination_dir = config.get('Local', 'destination-dir')
    maxmind_uri = config.get('MaxMind', 'uri')
    maxmind_files = config.items("Files")
    hipchat_logger = HipChatLogger(config._sections) 

    # Check directories exist
    if not os.path.isdir(download_dir):
        raise Exception("Download directory %s does not exist" % download_dir)
    if not os.path.isdir(destination_dir):
        raise Exception("Destination directory %s does not exist" % destination_dir)

    # Iterate through the files and download as necessary
    for _, remote in maxmind_files:

        local = os.path.basename(remote)
        zipped_file = os.path.join(download_dir, local)          
        return_code = mirror(maxmind_uri + remote, zipped_file)

        if (return_code >= 200 and return_code < 400) and return_code != 304:

            # Generate the unzipped filename
            local_file = os.path.splitext(local)[0]
            unzipped_file = os.path.join(download_dir, local_file)

            # Unzip the file 
            gz = gzip.open(zipped_file)
            out = open(unzipped_file, 'w')
            try:
                out.writelines(line for line in gz)
            finally:
                out.close()

            # Finally move the unzipped file, overwriting the old one
            final_file = os.path.join(destination_dir, local_file)
            os.rename(unzipped_file, final_file)

            # Created notification message, print and send to HipChat if poss
            notification = "Updated MaxMind database file %s" % final_file
            print notification
            hipchat_logger.notify(notification)

class HipChatLogger():
    """Simple class to handle notifications to HipChat. Wraps the Bash notification script rather than using python-hipchat (which is more complex)"""

    def __init__(self, config):
        """Prepare the HipChat notification command from the config's HipChat dict, if there is one"""

        if 'HipChat' in config:
            self.hipchat_command = "%(cli-path)s -t %(token)s -r %(room-id)s -c %(color)s -f \"%(from-name)s\"" % config['HipChat']
        else:
            self.hipchat_command = None

    def notify(self, message):
        """Send a message to HipChat"""

        if self.hipchat_command is not None:
            os.system("echo \"%s\" | %s" % (message, self.hipchat_command))

def mirror(uri, file):
    """Crude approximation of Perl's awesome mirror() function using urllib2"""

    # Start building the request
    req = urllib2.Request(uri)

    # Add the file's datestamp as the If-Modified-Since, if it exists
    if os.path.isfile(file):
        mtime = os.path.getmtime(file)
        if_modified_since = datetime.datetime.fromtimestamp(mtime).strftime("%a, %d %b %Y %H:%M:%S GMT") # e.g. Fri, 02 Feb 2010 22:04:23 GMT
        req.add_header("If-Modified-Since", if_modified_since)

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

class NotModifiedHandler(urllib2.BaseHandler):
    """Taken from http://www.artima.com/forums/flat.jsp?forum=122&thread=15024"""
 
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl

if __name__ == '__main__':
    controller()
