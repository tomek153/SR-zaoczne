import time
import dgl
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import torch
from pandas import CategoricalDtype
import numpy as np

columns = ["product_id", "product_price", "product_age_group", "product_gender", "product_brand", "product_category_1",
           "product_category_2", "product_category_3", "product_category_4", "product_category_5", "product_category_6",
           "product_category_7", "product_country", "product_title"]


def load_triples():
    df_triples = pd.read_csv('Triples/CSD_0C5663BE07C0228F28ECE1AA0BB59B25.csv')
    return df_triples


def generate_dgl_graph(df):
    # https://docs.dgl.ai/en/latest/generated/dgl.heterograph.html  = dokumentacja DGL Heterograph
    column_names = df.columns.values.tolist()
    # Destination list unique
    destination = df[column_names[0]].unique().tolist()
    # Source list unique
    source = df[column_names[-1]].unique().tolist()
    # Predicate list unique
    predicate = df[column_names[-2]].unique().tolist()

    destsource= set(destination + source)

    dfDestSource = pd.DataFrame(destsource, columns=['name'])

    categories = dfDestSource['name']
    cat_type = pd.CategoricalDtype(categories=categories, ordered=True)

    df[column_names[0]] = df[column_names[0]].astype(cat_type)
    df[column_names[-1]] = df[column_names[-1]].astype(cat_type)
    df['source_code'] = df[column_names[0]].cat.codes
    df['destination_code'] = df[column_names[-1]].cat.codes
    dataDict = {}
    for pred in predicate:
        relations = []
        src_list = df[df[column_names[-2]] == pred].source_code.tolist()
        dest_list = df[df[column_names[-2]] == pred].destination_code.tolist()
        relations.append(list(zip(src_list, dest_list)))
        for rel in relations:
            dataDict[('<' + column_names[0] + '>', '<' + pred + '>', '<' + column_names[-1] + '>')] = rel

    graph = dgl.heterograph(dataDict)
    return graph

# def convert_to_nx(dgl_graph):  # conversion from DGL to NX and drawing kamada kawai graph
#     dgl_metagraph = dgl_graph.metagraph()
#     graphNX = nx.MultiGraph()
#     graphNX.add_nodes_from(dgl_metagraph.nodes)
#     graphNX.add_edges_from(dgl_metagraph.edges)
#     pos = nx.kamada_kawai_layout(graphNX)
#     return nx.draw(graphNX, pos, with_labels=True)

def show_kamada_kawai(df):   # konwersja do nx.MultiGrpah i wygenerowanie grafu kamada_kawai
    G = nx.MultiGraph()
    relations = make_relation_list(df)
    G.add_edges_from(relations)
    pos = nx.kamada_kawai_layout(G)
    nx.draw_kamada_kawai(G, edge_color='grey')
    nx.draw_networkx_labels(G, pos)
    plt.show()

## POTRZEBNE DO MULTIPARTITE
## Zbudowanie relacji - listy krotek:

def make_relation_list(df):
    # Budowa listy relacji, złączenia: (0, 1), (1,2)
    relationList = []
    for index, row in df.iterrows():
        first = row[0]
        second = row[2]
        tuple = (first, second)
        relationList.append(tuple)
    return relationList

## POTRZEBNE DO MULTIPARTITE
## Przypisanie ID do wszystkich obiektów

def assign_IDs(df):
    predicates = {}
    objects = {}
    predcnt = 0
    objcnt = 0

    for index, row in df.iterrows():
        if row[0] not in predicates:
            predicates[row[0]] = predcnt
            predcnt = predcnt + 1

        if row[2] not in objects:
            objects[row[2]] = objcnt
            objcnt = objcnt + 1

    return predicates, objects


def show_Multipartite(df):
    G = nx.MultiGraph()
    nodes = assign_IDs(df)
    relations = make_relation_list(df)

    nodes_layer1 = []  # predicates list
    for n in nodes[0]:
        nodes_layer1.append(n)

    nodes_layer2 = []  # objects list
    for n in nodes[1]:
        nodes_layer2.append(n)

    G.add_nodes_from(nodes_layer1, layer=0)
    G.add_nodes_from(nodes_layer2, layer=1)
    print(nodes_layer2)
    G.add_edges_from(relations)
    pos = nx.multipartite_layout(G , subset_key="layer")
    return nx.draw(G, pos, with_labels=True, edge_color='green')

def metagraph_to_spring(dgl_graph): # konwersja grafu dgl_heterograph i wyświetlenie spring_layout
    # link do dokumentacji: https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
    dgl_metagraph = dgl_graph.metagraph()
    G = nx.MultiGraph()
    G.add_nodes_from(dgl_metagraph.nodes)
    G.add_edges_from(dgl_metagraph.edges)
    pos = nx.spring_layout(G)
    nx.draw_spring(G)
    #return nx.draw(G, pos)
    plt.show()

if __name__ == '__main__':
    # start time measure
    start = time.time()
    # load data from RDF
    df = load_triples()
    # Generate DGL Heterograph

    g = generate_dgl_graph(df)
    print("DGL Heterograph: \n")
    print(g)
    num_edges = {}
    g_etypes = g.canonical_etypes
    for etype in g_etypes:
        num_edges[etype] = g.number_of_edges(etype)

    # print('Liczba krawedzi'+str(num_edges))
    print("---------------------------------------")
    print("Rodzaje wierzcholkow grafu")
    print(g.ntypes)  # rodzaje wierzcholkow grafu
    print("---------------------------------------")
    print("Rodzaje krawedzi grafu")
    print(g.etypes)  # rodzaje krawedzi grafu
    print("---------------------------------------")

    # nx.draw(g.to_homogeneous().to_networkx())
    # nx.draw(gh, with_labels=True)
    print("Time: " + str(time.time() - start))

    ##### konwersja do NX i wyrysowanie grafu kamada kawai:
    #show_kamada_kawai(df)

    ##### konwersja do NX i wyrysowanie grafu multipartite:
    #show_Multipartite(df)   # graf nie uwzględnia hierarchii podkategorii

    ##### wyciągnięcie metagrafu i wyrysowanie grafu spring:
    #metagraph_to_spring(g)