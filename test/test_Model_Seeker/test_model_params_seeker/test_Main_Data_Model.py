from app.Model_Seeker.model_params_seeker.MainDataModel import MainDataModel
import pandas as pd



class TestMainDataModel:


    @classmethod
    def setup_method(cls):
        cls.df_test = pd.DataFrame()
        cls.data_model_test = MainDataModel(dataframe=cls.df_test, params={})


    def test_init_(self):

        assert self.data_model_test.df.empty is True
        assert self.data_model_test.params == {}
        assert self.data_model_test.new_dataframe is None
        assert self.data_model_test.new_target is None
        assert self.data_model_test.accuracy == 0
        assert self.data_model_test.count == 0