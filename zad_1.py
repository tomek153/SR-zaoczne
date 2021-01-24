import pandas as pd
import time

columns = ["product_id", "product_price", "product_age_group", "product_gender", "product_brand", "product_category_1", "product_category_2", "product_category_3", "product_category_4", "product_category_5", "product_category_6", "product_category_7", "product_country", "product_title"]
columns_final_to_change = ["product_id", "product_price", "product_age_group", "product_gender", "product_brand", "category", "product_country", "product_title"]
category_columns = ["product_category_1", "product_category_2", "product_category_3", "product_category_4", "product_category_5", "product_category_6", "product_category_7"]


def load_sets():
    df_all = pd.read_csv('Sets/CSD_0C5663BE07C0228F28ECE1AA0BB59B25.csv')
    return df_all[columns]


def get_category_from_categories_list(df):
    category_vector = []

    for index, row in df.iterrows():
        sub_category = None
        for col in category_columns:
            if str(row[col]) == "-1":
                if col == "product_category_1":
                    sub_category = "-1"
                break
            else:
                sub_category = row[col]
        category_vector.append(sub_category)

    return category_vector


def get_category_subclasses_triples_vector(df_category):
    category_subclasses_triples = []

    for index, row in df_category.iterrows():
        for i in range(len(category_columns)):
            if i != len(category_columns)-1:
                actual_el = str(row[category_columns[i]])
                next_el = str(row[category_columns[i+1]])

                if actual_el != "-1" and next_el != "-1":
                    category_subclasses_triples.append([actual_el, 'has_subcategory_of', next_el])
                else:
                    break

    df = pd.DataFrame(category_subclasses_triples, columns=['Subject', 'Predicate', 'Object'])
    return df.drop_duplicates()


def get_title_words_triples(df_title):
    title_words_triples = []

    for title in df_title:
        title = str(title)
        if title != "-1" and title != "" and title.lower() != "nan":
            for word in title.split(" "):
                title_words_triples.append([title, 'has_word', word])

    df = pd.DataFrame(title_words_triples, columns=['Subject', 'Predicate', 'Object'])
    return df.drop_duplicates()


def get_triples():
    df_data = load_sets()

    df_subcategory_triples = get_category_subclasses_triples_vector(df_data[category_columns])
    df_title_words_triples = get_title_words_triples(df_data['product_title'])

    category_vector = get_category_from_categories_list(df_data[category_columns])
    df_data["category"] = category_vector

    df_final = df_data[columns_final_to_change]
    df_final = df_final.rename(columns={'product_age_group': 'age', "product_gender": "gender", "product_brand": "brand", "product_country": "country", "product_title": "title"})
    columns_final = df_final.columns

    product_id = None
    triple_vector = []
    for index, row in df_final.iterrows():
        for col in columns_final:
            row_col = str(row[col])
            if col == "product_id":
                product_id = row_col
            else:
                if row_col != "-1" and row_col != "0.0" and row_col.lower() != "nan":
                    triple_vector.append([product_id, 'has_'+col, row[col]])

    df = pd.DataFrame(triple_vector, columns=['Subject', 'Predicate', 'Object'])
    df = df.drop_duplicates()

    df = df.append(df_subcategory_triples, ignore_index=True)
    df = df.append(df_title_words_triples, ignore_index=True)

    df.to_csv('./Triples/CSD_0C5663BE07C0228F28ECE1AA0BB59B25.csv', index=False)
    print(df)


if __name__ == '__main__':
    start = time.time()
    get_triples()
    print("Time: "+str(time.time()-start))
