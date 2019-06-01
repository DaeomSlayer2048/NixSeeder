import distros
import argparse
from tqdm import tqdm
import os
import urllib.request

#################################################################################################
#Globals
urls = {}

#################################################################################################
#Definitions
def get_torrents(distros, directory):
    for distro, urls in tqdm(distros.items(), desc="Distros"):
        for url in tqdm(urls, desc="Files"):
            filename = directory + url.rsplit('/', 1)[-1]
            exists = os.path.isfile(filename)
            if not exists:
                urllib.request.urlretrieve(url, filename)

#################################################################################################
#Arg parse
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

parser.add_argument("--Directory", help="Location to store torrent files", nargs='+')
args = parser.parse_args()

#################################################################################################
#Main
if args.Directory:
    directory = str(args.Directory[0])
    #Handle no ending slash
    if not directory.endswith('/'):
        directory = directory + '/'
else:
    directory = './Torrents/'
os.makedirs(directory, exist_ok=True)

urls['Ubuntu'] = distros.get_ubuntu()
urls['Arch'] = distros.get_arch()
urls['Fedora'] = distros.get_fedora()
get_torrents(urls, directory)
