import importlib
import pandas as pd


class UberModel(object):
    def __init__(self):
        """Main utility class for building Ubertool model classes for model execution."""
        super(UberModel, self).__init__()
        self.name = self.__class__.__name__
        self.inputs = None
        self.outputs = None
        self.outputs_expected = None

    def populate_inputs(self, pd_obj, model_obj):
        """
        Validate and assign user-provided model inputs to their respective class attributes
        :param pd_obj: Pandas DataFrame object of model input parameters
        :param model_obj:
        """

        module = importlib.import_module(
            '.' + model_obj.name.lower() + '_model_rest', 'REST_UBER.' + model_obj.name.lower() + '_rest')
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
        else:
            df['model'] = pd.Series(name=self.name)
            if df.columns.order().equals(pd_obj.columns.order()):
                # If the user-supplied DataFrame has the same column names as required by TerrplantInputs...
                # set each Series in the DataFrame to the corresponding TerrplantInputs attribute (member variable)
                for column in pd_obj.columns:
                    setattr(model_obj, column, pd_obj[column])
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

        module = importlib.import_module(
            '.' + model_obj.name.lower() + '_model_rest', 'REST_UBER.' + model_obj.name.lower() + '_rest')
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

    @staticmethod
    def get_dict_rep(model_obj):
        """
        Convert DataFrames to dictionary, returning a tuple (inputs, outputs, exp_out)
        :param model_obj: model instance
        :return: (dict(input DataFrame), dict(outputs DataFrame), dict(expected outputs DataFrame))
        """
        try:
            return model_obj.pd_obj.to_dict(), model_obj.pd_obj_out.to_dict(), model_obj.pd_obj_exp.to_dict()
        except AttributeError:
            return model_obj.pd_obj.to_dict(), model_obj.pd_obj_out.to_dict(), {}
