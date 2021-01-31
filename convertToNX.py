import networkx as nx
import matplotlib.pyplot as plt

from relations import *

path = "data-dev/"
file = "CSD_48D496922CDF10DE06AC91967B5C7F9C.csv"


def mappedRelation(_df):
    relationList = []
    for index, row in _df.iterrows():
        first = row[0]
        second = row[2]
        tuple = (first, second)
        relationList.append(tuple)
    return relationList


def showKawai(_df):
    print("Graph generation started...")
    G = nx.MultiGraph()
    rel = mappedRelation(_df)
    G.add_edges_from(rel)
    pos = nx.kamada_kawai_layout(G)
    nx.draw_kamada_kawai(G, edge_color='grey')
    nx.draw_networkx_labels(G, pos)
    print("Graph generated.")
    plt.show()


def showMultipartite(_df):
    print("Graph generation started...")
    G = nx.MultiGraph()
    rel = mappedRelation(_df)
    listOfNodes1 = [seq[0] for seq in mappedRelation(_df)]
    listOfNodes2 = [seq[1] for seq in mappedRelation(_df)]
    G.add_nodes_from(listOfNodes1, layer=0)
    G.add_nodes_from(listOfNodes2, layer=1)
    G.add_edges_from(rel)
    pos = nx.multipartite_layout(G, subset_key="layer")
    nx.draw(G, pos, with_labels=True, edge_color="grey")
    print("Graph generated.")
    plt.show()

if __name__ == '__main__':
    dfHasProductPrice = relationHasProductPrice(path, file)
    #showKawai(dfHasProductPrice)
    #showMultipartite(dfHasProductPrice)
