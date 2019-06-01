import re
import urllib.request

def get_ubuntu():
    version_urls = []
    urls = []
    base_url = "ftp://releases.ubuntu.com/releases/"
    torrent_format = re.compile("ubuntu-.+\.iso\.torrent")
    version_format = re.compile("[0-9]+\.[0-9]+\.[0-9]+|[0-9]+\.[0-9]+")
    #Get site
    response = urllib.request.urlopen(base_url).read().decode('utf-8')
    #Find versions
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
