import os
import re
import numpy as np
import pandas as pd
from Tool.functions import MemoryMatrix
from datetime import date


class MetfileMatrix(MemoryMatrix):
    def __init__(self, memmap_path, input_dir, start_date):
        self.input_dir = input_dir
        self.header = ["Month", "Day", "Year", "Precip", "PET", "Temp"]
        self.keyfile_path = os.path.join(memmap_path, "metfile_key.npy")
        self.start_date = start_date
        self.file_start_date, self.file_end_date = None, None

        self.metfiles = self.map_metfiles()
        self.metfile_ids, _ = zip(*self.metfiles)

        for i, (grid_id, data) in enumerate(self.read_metfiles()):
            if not (i + 1) % 25:
                print("{}/{}".format(i + 1, len(self.metfiles)))
            if not i:
                self.file_start_date, self.file_end_date = \
                    (date(*map(int, (data.iloc[i].Year, data.iloc[i].Month, data.iloc[i].Day))) for i in [0, -1])
                self.start_offset = (self.start_date - self.file_start_date).days
                self.end_date = self.file_end_date
                super(MetfileMatrix, self).__init__(self.metfile_ids, (self.file_end_date - self.start_date).days + 1,
                                                    3,
                                                    path=memmap_path, name="metfile", dtype=np.float32)
            out_rows = data.as_matrix()[self.start_offset:, 3:]
            self.update(grid_id, out_rows)

        convert_date = lambda d: d.strftime('%Y-%m-%d')
        key = np.array([convert_date(self.start_date), convert_date(self.end_date)] + list(self.metfile_ids))
        np.save(self.keyfile_path, key)

    def map_metfiles(self):
        metfile_map = {}
        for f in os.listdir(self.input_dir):
            match = re.match("(\d+?)_grid.wea", f)
            if match:
                grid_id = match.group(1)
                full_path = os.path.join(self.input_dir, f)
                metfile_map[grid_id] = full_path
        return sorted(metfile_map.items())

    def read_metfiles(self):
        for grid_id, grid_file in self.metfiles:
            grid_data = pd.read_csv(grid_file, index_col=False, names=self.header, usecols=range(6))
            yield grid_id, grid_data


def main():
    out_dir = r"..\bin\Preprocessed\MetTables"
    input_dir = r"T:\utool\qed_ubertool\ubertool_ecorest\ubertool\ubertool\sam\bin\Preprocessed\Met1991-2015"
    start_date = date(1991, 1, 1)
    MetfileMatrix(out_dir, input_dir, start_date)


main()