import pandas as pd
from app.Model_Seeker.model_params_seeker.MainDataModel import MainDataModel




class MNNModel(MainDataModel):


    def __init__(self, dataframe: pd.DataFrame, params: dict):
        super().__init__(dataframe=dataframe, params=params)

        



    def apply_parameters(self):
        home_serie_no = self.params.get("home_serie", 0)
        away_serie_no = self.params.get("away_serie", 0)
        abs_dif_pos_no = self.params.get("abs_dif_pos", 0)
        home_nul_prob_no = self.params.get("home_nul_prob", 1)
        away_nul_prob_no = self.params.get("away_nul_prob", 1)
        
        new_df = self.df.copy()
        new_df = new_df[new_df.home_nul_prob < home_nul_prob_no]
        new_df = new_df[new_df.away_nul_prob < away_nul_prob_no]
        new_df = new_df[new_df.home_serie >= home_serie_no]
        new_df = new_df[new_df.away_serie >= away_serie_no]
        new_df = new_df[new_df.abs_dif_pos >= abs_dif_pos_no]

        ret_df = new_df.drop("target", axis=1)
        ret_target = new_df["target"]
        return ret_df, ret_target



    @property
    def accuracy(self):
        uplet = self.new_target.value_counts()
        if uplet.empty:
            return 0.0  # pragma: no cover
        else:
            self.check_target_is_binary(uplet)
            if len(uplet) == 1:
                if 0 in uplet:   # pragma: no cover
                    accuracy = 1
                else:   # pragma: no cover
                    accuracy = 0
            else:
                accuracy = uplet[0]/(uplet[0] + uplet[1])

            return accuracy


    @property
    def count(self):
        uplet = self.new_target.value_counts()
        if uplet.empty:
            return 0  # pragma: no cover
        else:
            self.check_target_is_binary(uplet)
            if len(uplet) == 1:
                if 0 in uplet:  # pragma: no cover
                    count = uplet[0]
                else:  # pragma: no cover
                    count = 0
            else:
                count = uplet[0] + uplet[1]

            return count
    
    
    @staticmethod
    def check_target_is_binary(value_count: pd.Series):
        uplet = value_count
        if len(uplet) > 2:
            raise AttributeError(f"la target passée en parametre n'est pas binaire alors que le model DMMatchNonNul l'est"  # pragma: no cover
                                 f" la target devrait avoir comme valeur 0 si le match n'est pas nul et 1 si le match est"
                                 f" nul. target actuel : \n {uplet}")


