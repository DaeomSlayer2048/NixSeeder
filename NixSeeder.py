import argparse
import urllib.request
import os

def get_torrents(distros, directory):
    ## NOTE: Most likely location for adding progress bar
    for distro in distros:
        filename = directory + distro["Name"] + "_" + distro["Release"] + "_" + distro["Architecture"] + ".torrent"
        urllib.request.urlretrieve(distro["Link"], filename)

parser = argparse.ArgumentParser(
    prog='PROG',
    description='''
    A simple script to pull in torrernt files of our favorite Linux distros.
    ''',
    epilog='''
    TODO: Add progress bar
    TODO: Take config file
    '''
)

parser.add_argument("--All", help="Download all torrernt files for all distrobutions", action="store_true")
parser.add_argument("--Directory", help="Location to store torrent files", nargs='+')
args = parser.parse_args()

if args.Directory:
    directory = str(args.Directory[0])
    #Handle no ending slash
    if not directory.endswith('/'):
        directory = directory + '/'
else:
    directory = './'

#Remove later, Used to prove FTP and HTTP both work
files = [{
    "Name":"Ubuntu_Desktop",
    "Architecture":"x86_64",
    "Release":"19.04",
    "Link":"http://releases.ubuntu.com/19.04/ubuntu-19.04-desktop-amd64.iso.torrent"
    }, {
    "Name":"Ubuntu_Desktop",
    "Architecture":"x86_64",
    "Release":"12.04.5",
    "Link":"ftp://releases.ubuntu.com/releases/12.04/ubuntu-12.04.5-alternate-amd64.iso.torrent"
    }]

get_torrents(files, directory)
