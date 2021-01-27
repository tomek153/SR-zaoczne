import pandas as pd
import csv


class ConvertToDF:
    def __init__(self, _path, _csv):
        self.path = _path
        self.csv = _csv
        self.fullPath = self.path + self.csv

    def toList(self, _predicat, _rel, _object):
        predicat = '<' + _predicat + '> '
        object = '<' + _object + '> '
        list = []

        with open(self.fullPath, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                if row[_object] != "-1" and row[_predicat] != "-1":
                    triplet = [predicat + row[_predicat], _rel, object + row[_object]]
                    list.append(triplet)
        return list

    def listToDF(self, _predicat, _rel, _object):
        triplets = self.toList(_predicat, _rel, _object)
        df = pd.DataFrame(triplets, columns=[_predicat, _rel, _object])
        df.drop_duplicates(inplace=True)
        return df
