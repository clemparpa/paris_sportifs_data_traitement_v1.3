import pandas as pd  # pragma: no cover
from app.DTO_class.DTO_Match_Non_Nuls import CompNonNulsDataModel  # pragma: no cover
from app.CompetitionMetadata.FDO_competitions import FdoCompetitions  # pragma: no cover
import numpy as np  # pragma: no cover



def load_array_comp_data_set(comp_id):  # pragma: no cover

    data, target = CompNonNulsDataModel(comp_id).export_to_array()
    return data, target




def load_array_all_comp_data_set():  # pragma: no cover
    
    all_data_list = []
    all_target_list = []
    for comp_id in FdoCompetitions.leagues_list:
        data_comp, target_comp = CompNonNulsDataModel(comp_id=comp_id).export_to_list()
        if len(data_comp) > 0:
            all_data_list.extend(data_comp)
            all_target_list.extend(target_comp)
            

    ret_data_array = np.array(all_data_list)
    ret_target_array = np.array(all_target_list)
    return ret_data_array, ret_target_array



def load_df_comp_data_set(comp_id):  # pragma: no cover
    df = CompNonNulsDataModel(comp_id=comp_id).export_to_dataframe()
    return df



def load_df_all_comp_data_set():  # pragma: no cover

    df_list = []
    for comp_id in FdoCompetitions.leagues_list:
        df_list.append(CompNonNulsDataModel(comp_id=comp_id).export_to_dataframe())

    ret_df = pd.concat(df_list)
    return ret_df


