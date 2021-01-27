import networkx as nx
import matplotlib.pyplot as plt

from relations import *

path = "data-dev/"
file = "CSD_0D5142F537DA673DF1EA07F667340E3D.csv"


def mappedRelation(_df):
    relationList = []
    for index, row in _df.iterrows():
        first = row[0]
        second = row[2]
        tuple = (first, second)
        relationList.append(tuple)
    return relationList


def showKawai(_df):
    G = nx.MultiGraph()
    print('1')  # for debug
    rel = mappedRelation(_df)
    print('2')  # for debug
    G.add_edges_from(rel)
    print('3')  # for debug
    pos = nx.kamada_kawai_layout(G)
    print('4')  # for debug
    nx.draw_kamada_kawai(G, edge_color='grey')
    nx.draw_networkx_labels(G, pos)
    print('5')  # for debug
    plt.show()


if __name__ == '__main__':
    dfHasProductPrice = relationHasProductPrice(path, file)
    showKawai(dfHasProductPrice)
