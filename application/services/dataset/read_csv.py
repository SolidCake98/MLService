import pandas as pd
import re

#TODO посмотреть на библиотеку dask!!! и попытаться сравнить скорость обработки
class ReadCSVFile:

    def __init__(self, path, chunk_size = 5000):
        self.path = path
        self.chunk_size = chunk_size

    def get_header(self):
        fp = open(self.path)
        header = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",fp.readline()[:-1])
        fp.close()
        return header

    def read_small_chunck(self, pos = 0, chunk=30):
        next_pos = 0

        fp = open(self.path)        
        fp.seek(pos)

        lines = []
        
        if pos == 0:
            line = fp.readline()
                
        for i in range(chunk):
            line = fp.readline()
            if line == "":
                break
            lines.append(re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",line[:-1]))

        next_pos = fp.tell()
        fp.close()

        response ={
            'next_pos' : next_pos,
            'data': lines
        }

        return response

    def fast_anlysis(self):

        header = self.get_header()

        counts = {x: pd.Series(dtype=int) for x in header}

        i = 0
        response = {}
        for chunk in pd.read_csv(self.path, chunksize=self.chunk_size, names=header):
            if i > 1:
                break
            i += 1

            for x in header:
                counts[x] = counts[x].add(chunk[x].value_counts(), fill_value=0)

        for x in header:
            response[x] = {
                'unique': len(counts[x]),
            }

        return response