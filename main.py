#!/usr/bin/env python
import requests
import sys
import re
import json
from bs4 import BeautifulSoup

def scrape_daily(url):
    r = requests.get(url)
    r.raise_for_status()
    m = re.search(r'({"context":.+)\)', r.text)
    if not m:
        raise Exception("Unable to scrape Dailymotion URL!")
    html = m.group(1) 
    js = json.loads(html) 
    video = ""
    for q in ('1080', '720', '480', '380', '240', '144'):
        try:
            video = js['metadata']['qualities'][q][0]['url']
            break
        except KeyError:
            pass
    return video

def scrape_wrestling(url):
    if not "wrestlingfreak" in url:
        url = "http://wrestlingfreak.info/cgi-bin/" + url
    r = requests.get(url, headers={'Referer': 'http://watchwrestling.uno'})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    daily_iframe = soup.find("iframe", src=re.compile(r'dailymotion'))
    if not daily_iframe:
        raise Exception("Unable to scrape wrestling URL!")
    return daily_iframe['src']

def main():
    prefix = sys.argv[1]
    try:
        counter = int(sys.argv[2])
    except:
        counter = 1
    with open("page.html") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a"):
        daily_url = scrape_wrestling(a['href'])
        real_url = scrape_daily(daily_url)
        print "{} {}".format(real_url, prefix + str(counter) + ".mp4")
        counter += 1

if __name__ == "__main__":
    main()
