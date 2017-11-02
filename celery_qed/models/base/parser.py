class Parser(object):
    """
    This is a copy-and-paste, and then edited version of pandas.io.json.Parser() class.
    The intention is to "freeze" the functionality provided by this class without risk of
    breaking the method with future Pandas updates.

    This class will take a pandas.DataFrame and try to convert its axis into inferred data
    types. This is useful for DataFrames created from JSON, as the Python conversion process
    from JSON string to dictionary (json.loads) does not infer data types for keys.
        E.g. A JSON string with the key "0" will be a String when converted to a
        Python dictionary, instead of casting the key to an integer.

    Therefore, when converting that dictionary into a DataFrame, the indices will be of the wrong
    data type (string instead of int). This is problematic because, by default, a Series created
    without a given index is a sequence of zero-based integers. When performing arithmetic on two
    Series, one with a "0" the other with a 0 index (string vs int), the resulting Series will
    contain both indices, instead of one index.

    """

    def __init__(self, df, orient='columns', dtype=True):

        self.obj = df
        self.orient = orient
        self.dtype = dtype

    def convert_axes(self):
        """ try to convert axes """
        for axis in self.obj._AXIS_NUMBERS.keys():
            new_axis, result = self._try_convert_data(self.obj._get_axis(axis))
            if result:
                setattr(self.obj, axis, new_axis)

        return self.obj  # Return DataFrame with axis dtype inferred

    def _try_convert_data(self, data):
        """ try to parse a ndarray like into a column by inferring dtype """

        result = False

        if data.dtype == 'object':

            # try float
            try:
                data = data.astype('float64')
                result = True
            except:
                pass

        if data.dtype.kind == 'f':

            if data.dtype != 'float64':

                # coerce floats to 64
                try:
                    data = data.astype('float64')
                    result = True
                except:
                    pass

        # do't coerce 0-len data
        if len(data) and (data.dtype == 'float' or data.dtype == 'object'):

            # coerce ints if we can
            try:
                new_data = data.astype('int64')
                if (new_data == data).all():
                    data = new_data
                    result = True
            except:
                pass

        # coerce ints to 64
        if data.dtype == 'int':

            # coerce floats to 64
            try:
                data = data.astype('int64')
                result = True
            except:
                pass

        return data, result
