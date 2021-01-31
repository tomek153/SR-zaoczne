import pandas as pd
import csv
from convertToDF import ConvertToDF

path = "data-splitted/"
file = "CSD_48D496922CDF10DE06AC91967B5C7F9C.csv"

__all__ = ["relationHasProductPrice", "relationHasAge", "relationHasGender", "relationHasBrand", "relationHasCountry", "relationHasTitle"]


def relationHasProductPrice(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_product_price', 'product_price')
    return df


def relationHasAge(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_age', 'product_age_group')
    return df


def relationHasGender(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_gender', 'product_gender')
    return df


def relationHasBrand(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_brand', 'product_brand')
    return df


def relationHasCountry(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_country', 'product_country')
    return df


def relationHasTitle(_path, _file):
    converter = ConvertToDF(_path, _file)
    df = converter.listToDF('product_id', 'has_title', 'product_title')
    return df


if __name__ == '__main__':
    dfHasProductPrice = relationHasProductPrice(path, file)
    print(dfHasProductPrice)

    dfHasAge = relationHasAge(path, file)
    print(dfHasAge)

    dfHasGender = relationHasGender(path, file)
    print(dfHasGender)

    dfHasBrand = relationHasBrand(path, file)
    print(dfHasBrand)

    dfHasCountry = relationHasCountry(path, file)
    print(dfHasCountry)

    dfHasTitle = relationHasTitle(path, file)
    print(dfHasTitle)
