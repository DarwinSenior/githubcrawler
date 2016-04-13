from __future__ import unicode_literals 
import sys
from fire_tracker import *
import networkx as nx

def is_connected(T1,T2):
    t1 = T1.keys()
    t2 = T2.keys()
    return bool(len(set(t1).intersection(set(t2))))

if len(sys.argv) < 2:
    datapath = './fire_tracker/'
else:
    if sys.argv[1][-1] == '/':
        datapath = sys.argv[1]
    else:
        datapath = sys.argv[1]+'/'

seeds = read_seeds()
TuList = []
TdList = []
for seed in seeds:
    TuList.append(get_Tu(seed,datapath))
    TdList.append(get_Td(seed,datapath))

edgeList = []
Nseeds = len(seeds)
for i in range(Nseeds):
    for j in range(i,Nseeds):
        if is_connected(TuList[i],TuList[j]) or is_connected(TdList[i],TdList[j]):
            edgeList.append((i,j))

G = nx.Graph(edgeList)
comp = [z for z in nx.connected_components(G)]
print comp
