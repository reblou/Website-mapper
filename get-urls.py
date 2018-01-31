#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import matplotlib.pyplot as plt
import networkx as nx
import sys
import re
import os

visitedURLs = {}
stack = []
pages = 0

plt.figure(figsize=(25,25))
G = nx.Graph()

def extractName(url):
    matchObj = re.match(r'http[s]*://(.*)\..*$', url)
    return matchObj.group(1)

try:
    args = sys.argv
    url = args[1]
    website = extractName(url)
except:
    print "No arguments, please enter url as an argument"
    exit()

def findLinks(soup):
    atags = soup.find_all('a', href=True)
    links = []

    for tag in atags:
        links.append(tag['href'])

    return links

def addEdges(page, links):
    for link in links:
        G.add_edge(page, link)

def addLinks(link):
    try:
        visitedURLs[link]
    except:
        visitedURLs[link] = False
        stack.append(link)

def expandUrl(parent, url):
    matchObj = re.match(r'http[s]*', url)
    if not matchObj:
        try:
            visitedURLs[parent+url]
        except:
            return parent + url
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
    pages += 1
    valid = True

    try:
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page, "html5lib")
    except:
        valid = False

    if valid:
        links = findLinks(soup)
        for link in links:
            if absUrl(link):
                addLinks(url)

        G.add_node(url)
        G.add_nodes_from(links)
        addEdges(url, links)

        for link in links:
            print "- ", link

    try:
        traverse(stack.pop())
    except Exception as e:
        print(e)
        print "end of stack"
        return


traverse(url)
print "pages: ", pages
print "values in dict: ", len(visitedURLs)
"""
G.add_node(url)

html_page = urllib2.urlopen(url)
soup = BeautifulSoup(html_page, "html5lib")


xs = findLinks(soup)

for link in xs:
    visitedURLs = addToDictionary(visitedURLs, link)
    print expandUrl(url, link)

for key, visited in visitedURLs.items():
    if not visited:
        stack.append(key)



G.add_nodes_from(xs)
G = addEdges(G, url, xs)

"""
plt.subplot(111)
#plt.show()
options = {
    'node_color' : 'black',
    'node_size' : '100',
    'width' : 3
}

#nx.draw_spectral(G, node_color='black', node_size=100, width=3, with_labels=True, font_color='black')
#nx.draw_spectral(G, node_color='black', node_size=100, width=3)
nx.draw(G, node_color='black', node_size=100, width=3)

plt.savefig(website + ".png")
#os.system("feh " + website + ".png")
