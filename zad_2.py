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
    column_names = df.columns.values.tolist()
    # Destination list unique
    x = df[column_names[0]].unique().tolist()
    # Source list unique
    y = df[column_names[-1]].unique().tolist()
    # Predicate list unique
    z = df[column_names[-2]].unique().tolist()

    xyz = set(x + y)

    df1 = pd.DataFrame((xyz), columns=['name'])

    categories = df1['name']
    cat_type = pd.CategoricalDtype(categories=categories, ordered=True)

    df[column_names[0]] = df[column_names[0]].astype(cat_type)
    df[column_names[-1]] = df[column_names[-1]].astype(cat_type)
    df['source_code'] = df[column_names[0]].cat.codes
    df['destination_code'] = df[column_names[-1]].cat.codes
    dataDict = {}
    for pred in z:
        relations = []
        src_list = df[df[column_names[-2]] == pred].source_code.tolist()
        dest_list = df[df[column_names[-2]] == pred].destination_code.tolist()
        relations.append(list(zip(src_list, dest_list)))
        for rel in relations:
            dataDict[('<' + column_names[0] + '>', '<' + pred + '>', '<' + column_names[-1] + '>')] =  rel

    graph = dgl.heterograph(dataDict)
    return graph


if __name__ == '__main__':
    start = time.time()
    df = load_triples()
    g = generate_dgl_graph(df)
    print(g)
    num_edges = {}
    g_etypes = g.canonical_etypes
    for etype in g_etypes:
        num_edges[etype] = g.number_of_edges(etype)

    # print('Liczba krawedzi'+str(num_edges))
    print("---------------------------------------")
    print("rodzaje wierzcholkow grafu")
    print(g.ntypes)  # rodzaje wierzcholkow grafu
    print("---------------------------------------")
    print("rodzaje krawedzi grafu")
    print(g.etypes)  # rodzaje krawedzi grafu
    print("---------------------------------------")
    # print(g.metagraph)
    # nx.draw(g.to_networkx())
    # gh = dgl.to_homogeneous(g)
    # print(dgl.DGLHeteroGraph.is_multihraph(g))
    print(g.ndata)
    # nx.draw(gh, with_labels=True)
    # print("Time: " + str(time.time() - start))
