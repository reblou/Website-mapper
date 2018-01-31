#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import matplotlib.pyplot as plt
import networkx as nx
import sys
import re
import os
from collections import deque

visitedURLs = {}
stack = deque()
pages = 0

plt.figure(figsize=(20,20))
G = nx.Graph()

def extractName(url):
    matchObj = re.match(r'http[s]*://(.*)\..*$', url)
    return matchObj.group(1)

try:
    args = sys.argv
    rooturl = args[1]
    website = extractName(rooturl)
    print "webst: ", website
except:
    print "No arguments, please enter url as an argument"
    exit()

def findLinks(soup):
    atags = soup.find_all('a', href=True)
    links = []

    for tag in atags:
        match = re.match(re.escape(website), tag['href'])
        if re.search(r"\." + re.escape(website) + r"\.", tag['href'], re.IGNORECASE):
            print "appending", tag['href']
            links.append(tag['href'])

    return links

def addEdges(page, links):
    for link in links:
        G.add_edge(page, link)

def addLinks(link):
    try:
        val = visitedURLs[link]
    except:
        visitedURLs[link] = False
        print "--added to stack--"
        stack.append(link)

def expandUrl(parent, url):
    url = re.sub(r'\?.*$', "", url)
    matchObj = re.match(r'http[s]*', url)

    if not matchObj:
        return parent+url
    else:
        return url

def absUrl(url):
    matchObj = re.match(r'http[s]*', url)
    if not matchObj:
        return False
    else:
        return True

def traverse(url):
    global pages, stack
    print "traversing: ", url
    valid = True

    try:
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page, "html5lib")
        if (pages > 50):
            print "First 100 pages"
            return
        pages += 1
    except:
        valid = False

    if valid:
        links = findLinks(soup)
        for link in links:
            if link !=  url:
                addLinks(expandUrl(rooturl, link))

        G.add_node(url)
        G.add_nodes_from(links)
        addEdges(url, links)

        for link in links:
            print "- ", link
    else:
        print "not valid"

    try:
        traverse(stack.popleft())
    except Exception as e:
        print(e)
        print "end of stack"
        return


traverse(rooturl)
print "pages: ", pages
print "values in dict: ", len(visitedURLs)

plt.subplot(111)
options = {
    'node_color' : 'black',
    'node_size' : '100',
    'width' : 3
}

#nx.draw_spectral(G, node_color='black', node_size=100, width=3, with_labels=True, font_color='black')
#nx.draw_spectral(G, node_color='black', node_size=100, width=3)
nx.draw(G, node_color='black', node_size=100, width=3)

plt.savefig(website + ".png")
os.system("feh " + website + ".png &")
