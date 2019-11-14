import urlparse

import requests, re

url = "http://bditec.gov.bd/"
target_link = []


def extract_link_from(url):
    reponse = requests.get(url)
    return re.findall('(?:href=")(.*)"', reponse.content)


def crawl(url):
    href_link = extract_link_from(url)
    for link in href_link:
        link = urlparse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")[0]
        if url in link and link not in target_link:
            target_link.append(link)
            print(link)
            crawl(link)


crawl(url)
