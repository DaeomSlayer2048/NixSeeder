import distros
import argparse
from tqdm import tqdm
import os, sys
import urllib.request

#################################################################################################
#Globals
urls = {}
supported_distros = ['Ubuntu', 'Arch', 'Fedora', 'CentOS', 'OpenSUSE', 'Parrot', 'Xubuntu', 'Qubes', 'GhostBSD']
requested_distros = []

#################################################################################################
# Definitions
def get_torrents(distros, directory):
    for distro, urls in tqdm(distros.items(), desc="Distros"):
        for url in tqdm(urls, desc="Files  "):
            filename = directory + url.rsplit('/', 1)[-1]
            exists = os.path.isfile(filename)
            if not exists:
                try:
                    urllib.request.urlretrieve(url, filename)
                except urllib.error.URLError as e:
                    tqdm.write("Error retrieveing %s " % (str(url)))
                    tqdm.write(e.reason)

#################################################################################################
# Menu system
def distro_selection_menu(supported_distros):
    num_distros = len(supported_distros)
    requested_distros = []
    while True:
        i = 0
        clear_screen()
        print("Please select any of the currently supported distros.")
        print("You may only select one at a time.")
        if len(requested_distros) > 0:
            print("Currently selected distros: %s" % (str(requested_distros)))
        while i < num_distros:
            print("%s: %s" % (str(i), supported_distros[i]))
            i += 1
        print("-1: Exit")
        print("-2: All")
        user_selection = int(input("Selection: "))
        if user_selection == -1:
            break
        elif user_selection == -2:
            requested_distros = supported_distros
            break
        requested_distros.append(supported_distros[user_selection])
    return requested_distros

def collect_distro_files(requested_distros):
    urls = {}
    if 'Ubuntu' in requested_distros:
        print("Collecting Ubuntu.")
        urls['Ubuntu'] = distros.get_ubuntu()
    if 'Arch' in requested_distros:
        print("Collecting Arch.")
        urls['Arch'] = distros.get_arch()
    if 'Fedora' in requested_distros:
        print("Collecting Fedora.")
        urls['Fedora'] = distros.get_fedora()
    if 'CentOS' in requested_distros:
        print("Collecting CentOS.")
        urls['CentOS'] = distros.get_centos()
    if 'OpenSUSE' in requested_distros:
        print("Collecting OpenSUSE.")
        urls['OpenSUSE'] = distros.get_opensuse()
    if 'Parrot' in requested_distros:
        print("Collecting Parrot.")
        urls['Parrot'] = distros.get_parrot()
    if 'Xubuntu' in requested_distros:
        print("Collecting Xubuntu.")
        urls['xubuntu'] = distros.get_xubuntu()
    if 'Qubes' in requested_distros:
        print("Collecting Qubes.")
        urls['qubes'] = distros.get_qubes()
    if 'GhostBSD' in requested_distros:
        print("Collecting GhostBSD.")
        urls['ghostbsd'] = distros.get_ghostbsd()
    return urls

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

#################################################################################################
# Arg parse
parser = argparse.ArgumentParser(
    prog='PROG',
    description='''
    A simple script to pull in torrernt files of our favorite Linux distros.
    Files are not re-downloaded if they already exist.
    '''
)

parser.add_argument("--Directory", help="Location to store torrent files", nargs='+')
parser.add_argument("--All", help="Grab all distro files", action="store_true")
args = parser.parse_args()

#################################################################################################
# Main
if args.Directory:
    directory = str(args.Directory[0])
    #Handle no ending slash
    if not directory.endswith('/'):
        directory = directory + '/'
else:
    directory = './Torrents/'
os.makedirs(directory, exist_ok=True)

if args.All:
    urls = collect_distro_files(supported_distros)
    print("Collecting distro files now")
    get_torrents(urls, directory)
    sys.exit()

requested_distros = distro_selection_menu(supported_distros)
clear_screen()
print("Collecting distro URLs now")
urls = collect_distro_files(requested_distros)
print("Collecting distro files now")
get_torrents(urls, directory)
