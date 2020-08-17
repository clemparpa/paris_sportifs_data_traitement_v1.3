from app.Model_Seeker.model_params_seeker.DataModelMatchNonNul import MNNModel
import pandas as pd
import pytest


class TestMNNModel:

    @classmethod
    def setup_method(cls):
        cls.test_value_count_raiser = pd.Series([1, 2, 3])
        cls.test_dict_df = {"home_serie": [0, 1, 2, 3, 4], "away_serie": [0, 1, 2, 3, 4],
                            "abs_dif_pos": [1, 2, 3, 4, 5], "home_nul_prob": [0.10, 0.20, 0.30, 0.40, 0.50],
                            "away_nul_prob": [0.10, 0.20, 0.30, 0.40, 0.50],
                            "target": [0, 0, 0, 1, 0]}
        cls.test_df = pd.DataFrame.from_dict(data=cls.test_dict_df)
        cls.test_params = {"home_serie": 2, "away_serie": 2}
        cls.test_model = MNNModel(dataframe=cls.test_df, params=cls.test_params)
        cls.parametred_dict = {"home_serie": [2, 3, 4], "away_serie": [2, 3, 4],
                               "abs_dif_pos": [3, 4, 5], "home_nul_prob": [0.30, 0.40, 0.50],
                               "away_nul_prob": [0.30, 0.40, 0.50],
                               "target": [0, 1, 0]}
        cls.parametred_df = pd.DataFrame.from_dict(cls.parametred_dict)


    def test_check_target_is_binary(self):
        with pytest.raises(AttributeError):
            MNNModel(dataframe=pd.DataFrame(), params={}).check_target_is_binary(self.test_value_count_raiser)



    def test_apply_parameters(self):
        assert self.test_model.new_dataframe.reset_index(drop=True).equals(self.parametred_df.drop("target", axis=1)) is True
        assert self.test_model.new_target.reset_index(drop=True).equals(self.parametred_df["target"]) is True



    def test_accuracy(self):
        assert round(self.test_model.accuracy, 3 == round((1/3),3))


    def test_count(self):
        assert self.test_model.count == 3