#!/usr/bin/include python

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import networkx as nx

with open("google.html") as fp:
    soup = BeautifulSoup(fp, "html5lib")


links = soup.find_all('a')
xs = []

for l in links:
    print(l.get('href'))
    xs.append(l.get('href'))


G = nx.Graph()

G.add_nodes_from(xs)

plt.subplot(111)
#plt.show()
options = {
    'node_color' : 'black',
    'node_size' : '100',
    'width' : 3
}

#nx.draw(G, with_labels=True, font_weight='bold')
nx.draw_spectral(G, node_color='black', node_size=100, width=3, with_labels=True, font_color='black')

plt .savefig('1.png')
