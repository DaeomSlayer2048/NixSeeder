import re
import urllib.request

def parse_ftp(base_url, torrent_format, version_format):
    #A generic FTP directory parser with torrents stored in folders seperated by version
    urls = []
    version_urls = []
    #Get site
    response = urllib.request.urlopen(base_url).read().decode('utf-8')
    versions = version_format.findall(response)
    for version in versions:
        version_url = base_url + version + '/'
        version_urls.append(version_url)
    version_urls = list(set(version_urls))
    #Get torrents in version folder
    for version_url in version_urls:
        response = urllib.request.urlopen(version_url).read().decode('utf-8')
        torrents = torrent_format.findall(response)
        for torrent in torrents:
            url =  version_url + torrent
            print("Found: %s" % (url.rsplit('/', 1)[-1]))
            urls.append(url)
    return urls

def get_ubuntu():
    base_url = "ftp://releases.ubuntu.com/releases/"
    torrent_format = re.compile("ubuntu-.+\.iso\.torrent")
    version_format = re.compile("[0-9]+\.[0-9]+\.[0-9]+|[0-9]+\.[0-9]+")
    urls = parse_ftp(base_url, torrent_format, version_format)
    return urls

def get_arch():
    base_url = "ftp://mirror.rackspace.com/archlinux/iso/"
    torrent_format = re.compile("archlinux-.+\.iso\.torrent")
    version_format = re.compile("[0-9]+\.[0-9]+\.[0-9]+|[0-9]+\.[0-9]+")
    urls = parse_ftp(base_url, torrent_format, version_format)
    return urls

def get_fedora():
    urls = []
    base_url = "https://torrent.fedoraproject.org/torrents/"
    torrent_format = re.compile("(?:\"\>)(Fedora.+.torrent)")
    #Main page
    response = urllib.request.urlopen(base_url).read().decode('utf-8')
    torrents = torrent_format.findall(response)
    for torrent in torrents:
        url = base_url + torrent
        urls.append(url)
    return urls
