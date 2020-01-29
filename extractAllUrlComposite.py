import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

#Internal links are URLs that links to other pages of the same website.
#External links are URLs that links to other websites.

from abc import ABC, abstractmethod

class Component(ABC):

    def __init__(self, name):
        self.name = name

    def add(self, component):
        pass

    def remove(self, component):
        pass

    def getChilds(self):
        pass
    def is_composite(self):
        return False

    @abstractmethod
    def PrintTheUrl(self) -> str:
        pass

class Composite(Component):
    def __init__(self, name):
        super().__init__(name)
        self._children = set()

    def PrintTheUrl(self, space):
        print(space + self._name)
        for child in self._children:
            child.PrintTheUrl(space + "   ")

    def add(self, component):
        self._children.add(component)

    def getChilds(self):
        return self._children;

    def remove(self, component):
        self._children.discard(component)

    def is_composite(self):
        return True

class Leaf(Component):
    def __init__(self, name):
        super().__init__(name)

    def PrintTheUrl(self, space):
        print(space + self._name)

    def getChilds(self):
        return None;

    def is_composite(self):
        return False

def Draw(Comp, space):
    print(space + Comp.name)
    if Comp.getChilds() == None:
        return
    for component in Comp.getChilds():
        Draw(component, space + "   ")

def is_valid(url):
    """
    Checks whether `url` is a valid URL. (scheme and netloc exists in the URL)
    (not links to parts of the website, and not javascript)
    scheme = protocol, e.g http or https
    netloc = domain name
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


total_roots = 0
def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`,  I've used Python sets here because we don't want redundant links.
    urls = set()
    container = []
    global total_roots
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    root = Composite(url)
    global IsCrawling
    for a_tag in soup.findAll("a"):
        if not IsCrawling:
            break
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        container.append(Composite(href))
        internal_urls.add(href)
    print("====Root Print====")
    total_roots += 1
    for cont in container:
        root.add(cont)
    Draw(root,"")
    print("====Root Print====")
    return urls

# number of urls visited so far will be stored here
total_urls_visited = 0
# number of max urls to crawl, default is 10
max_urls=20
# bool - IsCrawling or stop the scan
IsCrawling = True

def crawl(url):
    """
    Crawls a web page and extracts all links recursively.
    However, i limited the URLs checked in order that the program will not be stuck.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is _.
    """
    global total_urls_visited
    global max_urls
    global IsCrawling
    if IsCrawling:
        total_urls_visited += 1
        links = get_all_website_links(url)
        for link in links:
            if total_urls_visited >= max_urls:
                break
            crawl(link) #recursive

def StopCrawl():
    global IsCrawling
    IsCrawling = False

if __name__ == "__main__":
    crawl("https://en.wikipedia.org/wiki/Astronomy")

    print("[+] Total External links:", len(external_urls))
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total:", len(external_urls) + len(internal_urls))

    print(f'total roots: {total_roots}')