# needs to be run whenever the qaqc csv is updated
import pandas as pd

csv_path = "./stir_qaqc.csv"
csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"

#skipfooter is rows from the bottom of the spreadsheet
pd_obj_inputs = pd.read_csv(csv_path, index_col=0, header=None, na_values=[''], skiprows=1, skipfooter=44, engine='python')
pd_obj_inputs = pd_obj_inputs.drop(labels=pd_obj_inputs.columns[range(4)], axis=1)
pd_obj_inputs.index.name = None
pd_obj_inputs.columns -= 5
pd_obj_inputs_transposed = pd_obj_inputs.transpose()
pd_obj_inputs_transposed.to_csv(csv_transpose_path_in)

#skiprows is number of rows from the top
pd_obj_exp_out = pd.read_csv(csv_path, index_col=0, header=None, na_values=[''], skiprows=40, engine='python')
pd_obj_exp_out = pd_obj_exp_out.drop(labels=pd_obj_exp_out.columns[range(4)], axis=1)
pd_obj_exp_out.index.name = None
pd_obj_exp_out.columns -= 5
pd_obj_exp_out_transposed = pd_obj_exp_out.transpose()
pd_obj_exp_out_transposed.to_csv(csv_transpose_path_exp)