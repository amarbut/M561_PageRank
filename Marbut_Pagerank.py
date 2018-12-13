# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 22:38:37 2018

@author: Administrator
"""

import pickle
import pandas as pd
import numpy as np
from collections import defaultdict


with open("outlinks.pkl", "rb") as f:
    outlinks = pickle.load(f)

#count number of distinct links scraped from 502 pages crawled
all_links = set()    
for link in outlinks:
    all_links.add(link)
    for outlink in outlinks[link]:
        all_links.add(outlink)
#4994 distinct urls collected altogether

#create df of source-outlink pairs, filtering for links that were crawled
link_df = pd.DataFrame(columns = ['source', 'outlink'])
for link in outlinks:
    for outlink in outlinks[link]:
        if outlink in outlinks:
            pair = pd.DataFrame([[link, outlink]], columns = ['source', 'outlink'])
            link_df = pd.concat([link_df, pair], ignore_index = True)

#create frequency df of dummy variables for each combination
sparse_links = pd.crosstab(index = link_df['source'], columns = link_df['outlink'])

#include pages crawled with no outlinks, or with no outlinks to other pages crawled
for link in outlinks:
    if link not in sparse_links.index:
        new_row = pd.DataFrame([[0]*502], index = [link], columns = sparse_links.columns)
        sparse_links = pd.concat([sparse_links, new_row])

# replace row values with link probability (ie. 1/number of outlinks from page)
for link in sparse_links.index:
    try:
        prob = 1/len([i for i in outlinks[link] if i in sparse_links.index])
        sparse_links[(sparse_links.index == link)] *= prob
    #if no outlinks, equal probability of going to any other page
    except ZeroDivisionError:
        sparse_links[(sparse_links.index == link)] = [[1/502]*502]
        pass

#reorder columns to be in the same order as rows
row_order = sparse_links.index.tolist()
sparse_links = sparse_links[row_order]

#convert dataframe to np array
#save row and column names in dictionaries

sources ={}
for idx, source in enumerate(sparse_links.index):
    sources[idx] = source

# convert to array with source urls as columns (ie. each column adds to 1)
linkArray = sparse_links.values.T

#add teleportation operation
d = 0.85
withTeleport = d * linkArray + (1-d)/502 * np.ones([502, 502]) 

#use power-iteration method to find pagerank eigenvector with eigenvalue of 1
# Sets up starting pagerank vector with equal rank for all pages
r = np.ones(502) / 502 
lastR = r
# calculate dot-product of transformation matrix (computed by link 
# probabilities and teleportation operation) and pagerank vector r
r = withTeleport @ r
i = 0 #count the number of iterations until convergence
#break loop once pagerank vector changes less than 0.0001
while np.linalg.norm(lastR - r) > 0.00001 :
    lastR = r
    r = withTeleport @ r
    i += 1
print(str(i) + " iterations to convergence.")

# match pagerank vector back up with source url labels
rankedUrls = []
for i in sources:
    pair = (sources[i], r[i])
    rankedUrls.append(pair)

# sort urls by pagerank to find highest ranking pages
sortedRank = sorted(rankedUrls, key = lambda tup: tup[1], reverse = True)
#print top 5 ranked pages
print(sortedRank[0:5])

#count inlinks
inlinks = {}
for page in outlinks:
    counter = 0
    for other_page in outlinks:
        if page in outlinks[other_page]:
            counter += 1
    inlinks[page] = counter

#save url, rank, number of inlinks, and number of outlinks to txt file for import into R for visualization
with open("sortedPageRank.txt", "w", encoding = "utf-8") as file:
    headers = ["url", "rank", "num_in"]
    file.write("\t".join(headers)+"\n")
    for pair in sortedRank:
        url, rank = pair
        num_in = inlinks[url]
        row = [url, str(rank), str(num_in)]
        file.write("\t".join(row)+"\n")

#create dictionary of inlinks for exploration
inlinkDict = defaultdict(list)
for page in outlinks:
    for other_page in outlinks:
        if page in outlinks[other_page]:
            inlinkDict[page].append(other_page)