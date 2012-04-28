#!/usr/bin/env python

"""maxmind-geolite-update: Updates the MaxMind geo IP databases"""

# Standard command-line imports
import os, sys, optparse
import ConfigParser

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
    mysql_host = config.get('Local', 'destination-dir')

    # MaxMind-specific vars 
    maxmind_root_uri = config.get('MaxMind', 'root-uri')

    # MaxMind:local file mappings
    maxmind_files = config._sections['Files']
    del maxmind_files['__name__']

    # Iterate through the files and download as necessary
    for local, remote in maxmind_files.iteritems():
        print "%s --> %s" % (remote, local)

if __name__ == '__main__':
    controller()
