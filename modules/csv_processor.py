import pandas as pd
from .database_handler import get_engine

class CsvProcessor():
    def __init__(self, spec_and_data: tuple) -> None:
        self.spec_filepath = spec_and_data[0]
        self.data_filepath = spec_and_data[1]
        self.conn_db = get_engine()
        self.tablename = self.spec_filepath.rsplit('/')[-1].rsplit('.', 1)[0]
    
    def load_schema(self) -> dict:
        df = pd.read_csv(self.spec_filepath)
        df['index'] = df.index
        schema_dict = df.groupby(['index'])[['column name', 'width', 'datatype']].apply(lambda g: g.values.tolist()).to_dict()
        del df
        for el in schema_dict:
            schema_dict[el] = [item for sublist in schema_dict[el] for item in sublist]
        self.schema_dict = schema_dict

    def load_data(self) -> pd.DataFrame:
        cols = [item[0] for item in self.schema_dict.values()]
        widths = [item[1] for item in self.schema_dict.values()]
        self.data = pd.read_fwf(self.data_filepath, header=None, widths=widths, names=cols)
        return self.data

    def write_data(self) -> None:
        self.data.to_sql(self.tablename, con=self.conn_db, if_exists='append', index=False)