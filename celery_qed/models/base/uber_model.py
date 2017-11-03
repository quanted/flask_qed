import importlib
import pandas as pd
from pandas import compat
from .parser import Parser
import logging


class UberModel(object):
    """
    Collection of static methods used across all the ubertool models.
    """

    def __init__(self):
        """Main utility class for building Ubertool model classes for model execution."""
        super(UberModel, self).__init__()
        self.name = self.__class__.__name__
        self.pd_obj = None
        self.pd_obj_exp = None
        self.pd_obj_out = None

    def validate_input_names(self, model_inputs, user_inputs):
        """
        Compare the user supplied inputs with the ModelInputs() class attributes, ensuring they match by name

        :param model_inputs: ModelInputs() class instance
        :return: Boolean
        """
        # Create temporary DataFrame where each column name is the same as ModelInputs attributes
        df = pd.DataFrame()
        for input_param in model_inputs.__dict__:
            df[input_param] = getattr(self, input_param)
        keys_a = set(getattr(self, input_param))
        keys_b = set(self.pd_obj.keys())
        extras = keys_b - keys_a
        n_extras = len(extras)
        print('There are {n_extras} extra keys.')
        print(extras)
        missing = keys_a - keys_b
        n_missing = len(missing)
        print('There are {n_missing} missing keys.')
        print(missing)
        # Compare column names of temporary DataFrame (created above) to user-supply DataFrame from JSON
        #if df.columns.sort_values().equals(user_inputs.columns.sort_values()):
        if n_extras >= 0 and n_missing == 0:
            print('Input parameters match what is expected.')
            print(set(df.keys()))
            return True
        else:
            print('Inputs parameters do not have all required inputs.')
            msg_err1 = "Inputs parameters do not have all required inputs. Please see API documentation.\n"
            msg_err2 = "Expected: \n{}\n".format(df.columns.sort_values())
            msg_err3 = "Received: \n{}\n".format(self.pd_obj.columns.sort_values())
            missing = [item for item in keys_a if item not in keys_b]
            msg_missing = "missing the following field(s): \n{}\n".format(missing)
            extras = [item for item in keys_b if item not in keys_a]
            msg_extras = "the following extra field(s) were found: \n{}\n".format(extras)
            print(msg_err1 + msg_err2 + msg_err3 + msg_missing + msg_extras)
            raise ValueError(msg_err1 + msg_err2 + msg_err3 + msg_missing + msg_extras)

    def coerce_input_dtype(self, incoming_dtype, coerce_dtype, input_series):
        #incoming_dtype = \
        logging.info(incoming_dtype)
        #incoming_dtype = 'float64'
        if coerce_dtype == 'object':
            return input_series.astype('object')
        elif coerce_dtype == 'float64':
            if incoming_dtype == 'object':
                #coerces strings to np.nans
                return pd.to_numeric(input_series, errors='coerce')
            elif incoming_dtype == 'float64':
                return input_series
            else:
                return input_series.astype('float64')
        elif coerce_dtype == 'int64' or 'int32':
            if incoming_dtype == 'object':
                #coerces strings to np.nans
                return pd.to_numeric(input_series, errors='coerce', downcast='int64')
            else:
                return input_series.astype('int64')
        else:
            print("dtype of {} is {}\n"
                  "This format is not handled by UberModel.coerce_input_dtype()".format(input_series.name, coerce_dtype))
            return input_series

    @staticmethod
    def convert_index(df_in):
        """ Attempt to covert indices of input DataFrame to duck typed dtype """
        parser = Parser(df_in)
        df = parser.convert_axes()
        return df

    def populate_inputs(self, df_in):
        """
        Validate and assign user-provided model inputs to their respective class attributes
        :param df_in: Pandas DataFrame object of model input parameters
        """
        df_user = self.convert_index(df_in)
        # mod_name = self.name.lower() + '.' + self.name.lower() + '_exe'
        mod_name = "ubertool.ubertool." + self.name.lower() + "." + self.name.lower() + '_exe'
        print(mod_name)
        try:
            # Import the model's input class (e.g. TedInputs) to compare user supplied inputs to
            module = importlib.import_module(mod_name)
            model_inputs_class = getattr(module, self.name + "Inputs")
            model_inputs = model_inputs_class()
        except ValueError as err:
            logging.info(mod_name)
            logging.info(err.args)

        try:
            if self.validate_input_names(model_inputs, df_user):
                # If the user-supplied DataFrame has the same column names as required by ModelInputs...
                # set each Series in the DataFrame to the corresponding ModelInputs attribute (member variable)
                # user_inputs_df = self._sanitize(df)
                for column in df_user.columns:
                    coerce_dtype = str(getattr(model_inputs, column).dtype)
                    df_series = df_user[column]
                    initial_dtype = str(df_series.dtype)
                    if initial_dtype != coerce_dtype:
                        logging.info('var:' + column + ' coerce to: ' + coerce_dtype + ' from: ' + initial_dtype)
                    setattr(self, column, self.coerce_input_dtype(initial_dtype, coerce_dtype, df_series))
        except ValueError as err:
            logging.info('input validation problem')
            logging.info(err.args)

    def populate_outputs(self):
        # Create temporary DataFrame where each column name is the same as *ModelName*Outputs attributes
        """
        Create and return Model Output DataFrame where each column name is a model output parameter
        :param model: string, name of the model as referred to in class names (e.g. terrplant, sip, stir, etc..)
        :param model_obj: class instance, instance of the model class for which the
        :return:
        """
        # Import the model's output class (e.g. TerrplantOutputs) to create a DF to store the model outputs in
        mod_name = self.name.lower() + '.' + self.name.lower() + '_exe'
        #mod_name = "ubertool_ecorest.ubertool.ubertool." + self.name.lower() + "." + self.name.lower() + '_exe'
        module = importlib.import_module(mod_name)
        model_outputs = getattr(module, self.name + "Outputs")
        model_outputs_obj = model_outputs()
        df = pd.DataFrame()
        for input_param in model_outputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)
            setattr(self, input_param, df[input_param])
        return df

    def fill_output_dataframe(self):
        """ Combine all output properties into Pandas Dataframe """
        for column in self.pd_obj_out.columns:
            try:
                output = getattr(self, column)
                print(output)
                if isinstance(output, pd.Series):
                    # Ensure model output is a Pandas Series. Only Series can be
                    # reliably put into a Pandas DataFrame.
                    self.pd_obj_out[column] = output
                else:
                    print('"{}" is not a Pandas Series. Returned outputs must be a Pandas Series'.format(column))
            except:
                print("output dataframe error on " + column)
        print('output dataframe')
        print(self.pd_obj_out)
        return

    def get_dict_rep(self):
        """
        Convert DataFrames to dictionary, returning a tuple (inputs, outputs, exp_out)
        :param model_obj: model instance
        :return: (dict(input DataFrame), dict(outputs DataFrame), dict(expected outputs DataFrame))
        """
        try:
            # TODO: resolve issue from self.pd_obj_exp and pd_obj_out being NONE
            if self.pd_obj_exp is None and self.pd_obj_out is None:
                return self.to_dict(self.pd_obj), {}, {}
            else:
                return self.to_dict(self.pd_obj), \
                    self.to_dict(self.pd_obj_out), \
                    self.to_dict(self.pd_obj_exp)
        except AttributeError:
            return self.to_dict(self.pd_obj), \
                   self.to_dict(self.pd_obj_out), \
                   {}

    @staticmethod
    def to_dict(df):
        """
        This is an override of the the pd.DataFrame.to_dict() method where the keys in
        return dictionary are cast to strings. This fixes an error where duck typing would
        sometimes allow non-String keys, which fails when Flask serializes the dictionary to
        JSON string to return the HTTP response.

        Original method returns: dict((str(k), v.to_dict()) for k, v in compat.iteritems(df))
        :param df:
        :return:
        """
        out = {}
        for k, v in compat.iteritems(df):
            col = k
            for row, value in compat.iteritems(v):
                out[col] = {str(row): value}
        return out


class ModelSharedInputs(object):
    def __init__(self):
        """
        Container for the shared model inputs amongst most models (e.g. version, chemical name, & PC Code)
        """
        super(ModelSharedInputs, self).__init__()
        self.csrfmiddlewaretoken = pd.Series([], dtype="object")
        self.version = pd.Series([], dtype="object")
        self.chemical_name = pd.Series([], dtype="object")
        self.pc_code = pd.Series([], dtype="object")
