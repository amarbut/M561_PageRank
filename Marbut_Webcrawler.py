# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 23:39:00 2018

@author: Administrator
"""

import requests
from lxml import html
from collections import defaultdict
import random
import pickle

#begin with website built to practice webscraping/crawling
url = "http://www.umt.edu/"

#initialize empty dictionary to store all outlinks
outlinks = defaultdict(list)

#navigate to starting site
site = requests.get(url)
tree = html.fromstring(site.content)

#collect all hyperlinks from page
links = tree.xpath("//body//*/a[contains(@href, 'http')]/@href")

#add links to dictionary entry
outlinks[url] = links
counter = 0
broken = set()
pagecount = 0
#loop through links until reaching 500 sites
while len(outlinks) <= 500:
    print("Looping through links for page:", counter)
    #ranodmly find new set of links to crawl if list is empty
    if not links:
        links = outlinks[random.choice(list(outlinks))]
    #break loop if counter reachese 1000 without len(outlinks) reaching 500; stuck in closed loop
    if counter > 1000:
        break
    for link in links:
        if pagecount >1000:
            break
        #skip pages that have already been crawled
        if link not in outlinks and link not in broken:
            pagecount += 1
            print("Pulling links for page:", pagecount)
    
            #navigate to page
            try:
                site = requests.get(link)
                tree = html.fromstring(site.content)
                #pull all outlinks from page
                sublinks = tree.xpath("//body//*/a[contains(@href, 'http')]/@href")
                #add outlinks to dictionary entry
                outlinks[link] = sublinks
            except:
                broken.add(link)
                print("Error with ", link, ". Skipping")
                pass
    counter += 1
    links = sublinks

#save network as pickle object
with open("outlinks.pkl", "wb") as f:
    pickle.dump(outlinks, f)