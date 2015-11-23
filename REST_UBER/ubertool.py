import importlib
import pandas as pd


class UberModel(object):
    # TODO: Move this base class, UberModel, into its own utility module. This class is inherited by all Ubertool models
    def __init__(self):
        """
        Main utility class for building Ubertool model classes for model execution.
        """
        super(UberModel, self).__init__()
        self.name = self.__class__.__name__
        self.inputs = None
        self.outputs = None
        self.outputs_expected = None

    def populate_inputs(self, pd_obj, model_obj):
        """
        Validate and assign user-provided model inputs to their respective class attributes
        :param model:
        :param model_obj:
        :param pd_obj: Pandas DataFrame object of model input parameters
        """

        module = importlib.import_module('.' + model_obj.name.lower() + '_model_rest', model_obj.name.lower() + '_rest')
        ModelInputs = getattr(module, model_obj.name + "Inputs")
        model_inputs_obj = ModelInputs()

        # Create temporary DataFrame where each column name is the same as TerrplantInputs attributes
        df = pd.DataFrame()
        for input_param in model_inputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)

        # Compare column names of temporary DataFrame (created above) to user-supply DataFrame from JSON
        if df.columns.order().equals(pd_obj.columns.order()):
            # If the user-supplied DataFrame has the same column names as required by TerrplantInputs...
            # set each Series in the DataFrame to the corresponding TerrplantInputs attribute (member variable)
            for column in pd_obj.columns:
                setattr(model_obj, column, pd_obj[column])
            pass
        else:
            raise ValueError("Inputs parameters do not have all required inputs. Please see API documentation.")

    def populate_outputs(self, model_obj):
        # Create temporary DataFrame where each column name is the same as TerrplantOutputs attributes
        """
        Create and return Model Output DataFrame where each column name is a model output parameter
        :param model: string, name of the model as referred to in class names (e.g. terrplant, sip, stir, etc..)
        :param model_obj: class instance, instance of the model class for which the
        :return:
        """

        module = importlib.import_module('.' + model_obj.name.lower() + '_model_rest', model_obj.name.lower() + '_rest')
        ModelOutputs = getattr(module, model_obj.name + "Outputs")
        model_outputs_obj = ModelOutputs()
        df = pd.DataFrame()
        for input_param in model_outputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)
            setattr(model_obj, input_param, df[input_param])
        return df

    def fill_output_dataframe(self, model_obj):
        for column in model_obj.pd_obj_out:
            model_obj.pd_obj_out[column] = getattr(model_obj, column)

    def get_json(self, model_obj):
        """
        Convert DataFrames to JSON, returning a tuple
        of JSON strings (inputs, outputs, exp_out)
        :param pd_obj:
        :param pd_obj_out:
        :param pd_obj_exp:
        :return: ( , , )
        """

        pd_obj_json = model_obj.pd_obj.to_json()
        pd_obj_out_json = model_obj.pd_obj_out.to_json()
        try:
            pd_obj_exp_json = model_obj.pd_obj_exp.to_json()
        except:
            pd_obj_exp_json = "{}"

        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json