import operator
import itertools
import pandas as pd
from app.Model_Seeker.model_params_seeker.MainDataModel import MainDataModel


def check_parameter_in_model(dataframe: pd.DataFrame, params: dict):

    for key, values in params.items():
        if key not in list(dataframe.columns):
            raise AttributeError(f"Les paramètres du ParamSeeker a appliquer au model de donnés sont erronés:"
                                 f" la colonne : '{key}' n'existe pas dans le dataframe passé en paramètre ayant pour colonne"
                                 f" {list(dataframe.df.columns)}")

        if not isinstance(values, list):
            raise AttributeError(f"les valeurs de chaque clés du ditionnaire de paramètres doivent être des listes;"
                                 f" la clé '{key}' ne contient pas une list mais un objet de type: {type(values)} ")



def get_params_list(parameters: dict):
    list_params_key_list = []
    for key, values in parameters.items():
        key_dict_list = []
        for val in values:
            key_val_dict = {f"{key}": val}
            key_dict_list.append(key_val_dict)

        list_params_key_list.append(key_dict_list)

    params_tuple_list = list(itertools.product(*list_params_key_list))
    params_dict_list = []
    for uplet in params_tuple_list:
        params_dict = {}
        for dic in uplet:
            params_dict.update(dic)
        params_dict_list.append(params_dict)

    return params_dict_list



class ParamSeeker:  # pragma: no cover


    def get_best_model(self, sample_required: int) -> dict:
        model_list = []
        check_parameter_in_model(dataframe=self.dataframe, params=self.parameters)
        params_dict_list = get_params_list(self.parameters)
        for dic in params_dict_list:
            model_list.append(self.data_model(dataframe=self.dataframe, params=dic))

        model_acc_dict_list = []
        for model in model_list:
            if model.count >= sample_required:
                dict_model_acc = {"model_count": model.count, "model_data": model.new_dataframe, "model_params": model.params, "model_accuracy": model.accuracy}
                model_acc_dict_list.append(dict_model_acc)


        best_model = sorted(model_acc_dict_list, key=operator.itemgetter('model_accuracy'), reverse=True)
        return best_model[0]


    def __init__(self, data_model: MainDataModel.__subclasses__(), dataframe: pd.DataFrame, parameters: dict, sample_required: int):
        self.data_model = data_model
        self.parameters = parameters
        self.dataframe = dataframe
        self.best_model_dict = self.get_best_model(sample_required=sample_required)
        self.best_params = self.best_model_dict["model_params"]
        self.best_accuracy = self.best_model_dict["model_accuracy"]
        self.best_model_data = self.best_model_dict["model_data"]
        self.best_model_count = self.best_model_dict["model_count"]



"""dico_test = {"a": [1, 2, 3], "b": ["bob", "tom", "jo"]}
a = get_list_params_key_list(dico_test)
for els in a:
    print(els)"""

#data_model:
    #une property 'accuracy'
    #un attribut 'df'
    #un attribut 'params'
    # une property 'count'