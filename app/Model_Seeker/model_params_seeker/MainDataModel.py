import pandas as pd





class MainDataModel:


    def __init__(self, dataframe: pd.DataFrame, params: dict):
        self.df = dataframe
        self.params = params
        self.new_dataframe, self.new_target = self.apply_parameters()


    def apply_parameters(self):
        return None, None


    @property
    def accuracy(self):
        return 0


    @property
    def count(self):
        return 0
