import os
import numpy as np
import pandas as pd

from collections import OrderedDict
from dbfread import DBF, FieldParser


class NHDTable(pd.DataFrame):
    def __init__(self, region, path):
        super().__init__()
        self.region = region
        self.path = path
        self.table_path = os.path.join(path, "region_{}.npz".format(region))

        data, header = self.read_table()
        super(NHDTable, self).__init__(data=data, columns=header)

    def read_table(self):
        assert os.path.isfile(self.table_path), "Table not found for region {} in {}".format(self.region, self.path)
        data = np.load(self.table_path)
        return data['table'], data['key']


def read_dbf(dbf_file):
    class MyFieldParser(FieldParser):
        def parse(self, field, data):
            try:
                return FieldParser.parse(self, field, data)
            except ValueError:
                return None
    try:
        dbf = DBF(dbf_file)
        table = pd.DataFrame(iter(dbf))
    except ValueError:
        dbf = DBF(dbf_file, parserclass=MyFieldParser)
        table = pd.DataFrame(iter(dbf))
    table.rename(columns={column: column.lower() for column in table.columns}, inplace=True)
    return table


nhd_states = OrderedDict((('01', {"ME", "NH", "VT", "MA", "CT", "RI", "NY"}),
                          ('02', {"VT", "NY", "PA", "NJ", "MD", "DE", "WV", "DC", "VA"}),
                          ('03N', {"VA", "NC", "SC", "GA"}),
                          ('03S', {"FL", "GA"}),
                          ('03W', {"FL", "GA", "TN", "AL", "MS"}),
                          ('04', {"WI", "MN", "MI", "IL", "IN", "OH", "PA", "NY"}),
                          ('05', {"IL", "IN", "OH", "PA", "WV", "VA", "KY", "TN"}),
                          ('06', {"VA", "KY", "TN", "NC", "GA", "AL", "MS"}),
                          ('07', {"MN", "WI", "SD", "IA", "IL", "MO"}),
                          ('08', {"MO", "KY", "TN", "AR", "MS", "LA"}),
                          ('09', {"ND", "MN", "SD"}),
                          ('10U', {"MT", "ND", "WY", "SD", "MN", "NE", "IA"}),
                          ('10L', {"CO", "WY", "MN", "NE", "IA", "KS", "MO"}),
                          ('11', {"CO", "KS", "MO", "NM", "TX", "OK", "AR", "LA"}),
                          ('12', {"NM", "TX", "LA"}),
                          ('13', {"CO", "NM", "TX"}),
                          ('14', {"WY", "UT", "CO", "AZ", "NM"}),
                          ('15', {"NV", "UT", "AZ", "NM", "CA"}),
                          ('16', {"CA", "OR", "ID", "WY", "NV", "UT"}),
                          ('17', {"WA", "ID", "MT", "OR", "WY", "UT", "NV"}),
                          ('18', {"OR", "NV", "CA"})))

