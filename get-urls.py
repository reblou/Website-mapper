#!/usr/bin/include python

from bs4 import BeautifulSoup
import urllib2
import matplotlib.pyplot as plt
import networkx as nx
import sys
import re
import os

def findLinks(soup):
    atags = soup.find_all('a', href=True)
    links = []

    for tag in atags:
        links.append(tag['href'])

    return links

def addEdges(graph, page, links):
    for link in links:
        graph.add_edge(page, link)
    return graph

def extractName(url):
    matchObj = re.match(r'http[s]*://(.*)\..*$', url)
    return matchObj.group(1)

def addToDictionary(dict, key):
    try:
        val = dict[key]
    except:
        dict[key] = False
    return dict

def traverseWebsite(graph, url, visited, stack):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page, "html5lib")

    graph.add_node(url)

    links = findLinks(soup)

    for link in links:
        visitedURLs = addToDictionary(visitedURLs, link)

    for key, visited in visitedURLs.items():
        if not visited:
            print key
            stack.append(key)

    return graph


try:
    args = sys.argv
    url = args[1]
    website = extractName(url)
except:
    print "No arguments, please enter url as an argument"
    exit()


plt.figure(figsize=(10,10))
G = nx.Graph()
G.add_node(url)

html_page = urllib2.urlopen(url)
soup = BeautifulSoup(html_page, "html5lib")


links = soup.find_all('a')
xs = findLinks(soup)

visitedURLs = {url: True}
stack = []


for link in xs:
    visitedURLs = addToDictionary(visitedURLs, link)

for key, visited in visitedURLs.items():
    if not visited:
        print key
        stack.append(key)

while stack != []:
    url = stack.pop()
    if visitedURLs[url]:
        continue
    try:
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page, "html5lib")
    except:
        print "invalid link"
        visitedURLs[url] = True
        continue

    links = findLinks(soup)

    visitedURLs[url] = True
    for link in links:
        visitedUrls = addToDictionary(visitedURLs, link)

    for key, visited in visitedURLs.items():
        if not visited:
            stack.append(key)


G.add_nodes_from(xs)
G = addEdges(G, url, xs)

plt.subplot(111)
#plt.show()
options = {
    'node_color' : 'black',
    'node_size' : '100',
    'width' : 3
}

#nx.draw_spectral(G, node_color='black', node_size=100, width=3, with_labels=True, font_color='black')
nx.draw_spectral(G, node_color='black', node_size=100, width=3)
nx.draw(G, node_color='black', node_size=100, width=3)

plt.savefig(website + ".png")
os.system("feh " + website + ".png")
