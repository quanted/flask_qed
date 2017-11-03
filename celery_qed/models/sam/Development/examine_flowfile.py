import os
import numpy as np
from Tool.functions import MemoryMatrix


class FlowMatrix(MemoryMatrix):
    def __init__(self, region, file_path):
        self.region = region

        # Load key
        self.key_file = os.path.join(file_path, "region_{}_key.npy".format(self.region))
        self.reaches = np.load(self.key_file, mmap_mode='r')

        # Initialize matrix
        super(FlowMatrix, self).__init__(self.reaches, 2, 12, name="region_{}".format(self.region),
                                         path=file_path, input_only=True)


    def fetch(self, reach_id, data="flow", verbose=False):
        """ Pull flow or surface area data for the reach, then extend to match dates (select monthly values) """
        assert data in ("flow", "surface area"), "Invalid request for {}: must be 'flow' or 'surface area'".format(data)
        index = 0 if data == "flow" else 1
        record = super(FlowMatrix, self).fetch(reach_id, verbose)
        if record is not None:
            return record[index]


region = '02'
file_path = os.path.join("..", "bin", "Preprocessed", "FlowFiles")

flows = FlowMatrix(region, file_path)

for reach in flows.index:
    print(reach)
    print(flows.fetch(reach, 'flow'))
    print(flows.fetch(reach, 'surface area'))
    input()