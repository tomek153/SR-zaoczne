import time
import dgl
import pandas as pd
from pandas import CategoricalDtype
import numpy as np

columns = ["product_id", "product_price", "product_age_group", "product_gender", "product_brand", "product_category_1", "product_category_2", "product_category_3", "product_category_4", "product_category_5", "product_category_6", "product_category_7", "product_country", "product_title"]


def load_triples():
    df_triples = pd.read_csv('Triples/CSD_0C5663BE07C0228F28ECE1AA0BB59B25.csv')
    return df_triples

def generate_dgl_graph(df):
    relations = []
    column_names = df.columns.values.tolist()
    x = df[column_names[0]].unique().tolist()
    y = df[column_names[-1]].unique().tolist()
    xy = set(x+y)

    df1 = pd.DataFrame((xy),columns=['name'])

    categories = df1['name']
    cat_type = pd.CategoricalDtype(categories=categories, ordered=True)

    df[column_names[0]] = df[column_names[0]].astype(cat_type)
    df[column_names[-1]] = df[column_names[-1]].astype(cat_type)
    df['source_code'] = df[column_names[0]].cat.codes
    df['destination_code'] = df[column_names[-1]].cat.codes

    src_list = df.source_code.tolist()
    dest_list = df.destination_code.tolist()
    relations.append(list(zip(src_list,dest_list)))
    dataDict = {
        ('<'+column_names[0]+'>', '<'+column_names[1]+'>', '<'+column_names[-1]+'>'): relations[0],
    }
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

    #print('Liczba krawedzi'+str(num_edges))

    print(g.ntypes) # rodzaje wierzcholkow grafu
    print(g.etypes) # rodzaje krawedzi grafu

    #print("Time: " + str(time.time() - start))