import re
import urllib.request

static_directory = '/'

###########################################################################################
# Generic functions

def get_url(url):
    try:
        response = urllib.request.urlopen(url).read().decode('utf-8')
        return response
    except urllib.error.URLError as e:
        print("Error retrieveing %s " % (str(url)))
        print(e.reason)

def get_releases(base_url, release_format, static_directory):
    release_urls = []
    #Get site
    response = get_url(base_url)
    releases = release_format.findall(response)
    for release in releases:
        release_url = base_url + release + static_directory
        release_urls.append(release_url)
    #Remove dupes
    release_urls = list(set(release_urls))
    return release_urls

def get_urls(release_urls, torrent_format):
    urls = []
    #Get torrents in release folder
    for release_url in release_urls:
        response = get_url(release_url)
        torrents = torrent_format.findall(response)
        for torrent in torrents:
            url =  release_url + torrent
            print("Found: %s" % (url.rsplit('/', 1)[-1]))
            urls.append(url)
    #Remove dupes
    urls = list(set(urls))
    return urls

###########################################################################################
# Distros with generic/common directory structures
def get_ubuntu():
    base_url = "ftp://releases.ubuntu.com/releases/"
    torrent_format = re.compile("ubuntu-.+\.iso\.torrent")
    release_format = re.compile("[0-9]+\.[0-9]+\.[0-9]+|[0-9]+\.[0-9]+")
    release_urls = get_releases(base_url, release_format, static_directory)
    urls = get_urls(release_urls, torrent_format)
    return urls

def get_arch():
    base_url = "ftp://mirror.rackspace.com/archlinux/iso/"
    torrent_format = re.compile("archlinux-.+\.iso\.torrent")
    release_format = re.compile("[0-9]+\.[0-9]+\.[0-9]+|[0-9]+\.[0-9]+")
    release_urls = get_releases(base_url, release_format, static_directory)
    urls = get_urls(release_urls, torrent_format)
    return urls

def get_opensuse():
    static_directory = '/iso/'
    base_url = "ftp://www.gtlib.gatech.edu/pub/opensuse/distribution/leap/"
    torrent_format = re.compile("openSUSE\S+\.iso\.torrent")
    release_format = re.compile("[0-9]\.[0-9]|[0-9]+[0-9]\.[0-9]+")
    release_urls = get_releases(base_url, release_format, static_directory)
    urls = get_urls(release_urls, torrent_format)
    return urls

def get_parrot():
    base_url = "https://download.parrotsec.org/parrot/iso/"
    torrent_format = re.compile("(?:title=\")(.+\.torrent)(?!</a>)")
    release_format = re.compile("(?:title=\")(\d+\.\d+\.\d+|\d+.\d+|\d+)(?:\")")
    release_urls = get_releases(base_url, release_format, static_directory)
    urls = get_urls(release_urls, torrent_format)
    return urls

def get_gallium():
    urls = []
    static_directory = '/TORRENTS/'
    base_url = "https://galliumos.org/releases/"
    torrent_format = re.compile("galliumos.+?\.iso\.torrent")
    release_format = re.compile("[0-9]\.[0-9]\.[0-9]+|[0-9]\.[0-9]+")
    release_urls = get_releases(base_url, release_format, static_directory)
    urls = get_urls(release_urls, torrent_format)
    return urls

###########################################################################################
# Simple HTML

def get_xubuntu():
    #All files are on one page
    base_url = "https://xubuntu.org/download/"
    torrent_format = re.compile("http://torrent.+?\.iso\.torrent")
    response = get_url(base_url)
    urls = torrent_format.findall(response)
    urls = list(set(urls))
    for url in urls:
        print("Found: %s" % (url.rsplit('/', 1)[-1]))
    return urls

def get_ghostbsd():
    #All files are on one page
    base_url = "https://ghostbsd.org/download"
    torrent_format = re.compile("https://.+?\.torrent")
    response = get_url(base_url)
    urls = torrent_format.findall(response)
    urls = list(set(urls))
    for url in urls:
        print("Found: %s" % (url.rsplit('/', 1)[-1]))
    return urls

def get_qubes():
    #All files are on one page
    base_url = "https://www.qubes-os.org/downloads/"
    torrent_format = re.compile("https://.+?\.torrent")
    response = get_url(base_url)
    urls = torrent_format.findall(response)
    urls = list(set(urls))
    for url in urls:
        print("Found: %s" % (url.rsplit('/', 1)[-1]))
    return urls

###########################################################################################
# Distros with un-common / non-generic structures

def get_fedora():
    #Fedora torrents are all hosted in one top directory
    urls = []
    base_url = "https://torrent.fedoraproject.org/torrents/"
    torrent_format = re.compile("(?:\"\>)(Fedora.+\.torrent)")
    #Main page
    response = get_url(base_url)
    torrents = torrent_format.findall(response)
    for torrent in torrents:
        print("Found: %s" % (torrent))
        url = base_url + torrent
        urls.append(url)
    return urls

def get_centos():
    urls = []
    base_url = "ftp://mirror.rackspace.com/CentOS/"
    torrent_format = re.compile("CentOS-.+\.torrent")
    release_format = re.compile("[0-9]\.[0-9]\.[0-9]+|[0-9]\.[0-9]+")
    #Main page
    response = get_url(base_url)
    releases = release_format.findall(response)
    #Only the latest is stored on this server
    latest = max(releases)
    release_url = base_url + latest + '/isos/x86_64/'
    response = get_url(release_url)
    torrents = torrent_format.findall(response)
    for torrent in torrents:
        url =  release_url + torrent
        print("Found: %s" % (torrent))
        urls.append(url)
    return urls

###########################################################################################
#  Under construction
def get_debian():
    #COMBAK
    base_url = "ftp://cdimage.debian.org/cdimage/release/"
    release_format = re.compile("[0-9]\.[0-9]\.[0-9]\-live|[0-9]\.[0-9]\.[0-9]")
    arch_format = re.compile("(?!\s)[aimps][mr3iup]\w+-arch|(?:\s)[aimps][mr3iup]\w+")
    release_urls = get_releases(base_url, release_format, static_directory)
    static_directory = "/bt-hybrid/"
    #Get Release
    for release_url in release_urls:
        response = get_url(release_url)
        archs = arch_format.findall(response)
        for arch in archs:
            url = static_directory + arch + static_directory
            torrents = torrent_format.findall(response)
    return urls
