from app.Model_Seeker.model_params_seeker import ParamSeekerClass as script
import pandas as pd
import pytest


class TestCheckParameterInModel:

    @classmethod
    def setup_method(cls):
        cls.dico_test_no_seq = {"field_1": [1, 2, 3], "field_2": 0}
        cls.df = pd.DataFrame.from_dict({"field_1": [0], "field_2": [0]})
        cls.dico_no_match_column = {"field_3": [1, 3, 4]}

    def test_func_no_seq_dict(self):
        with pytest.raises(AttributeError):
            script.check_parameter_in_model(self.df, self.dico_test_no_seq)

    def test_func_columns_not_match(self):
        with pytest.raises(AttributeError):
            script.check_parameter_in_model(self.df, self.dico_no_match_column)


class TestGetParamsList:

    @classmethod
    def setup_method(cls):
        cls.dict_test = {"a": [0, 1], "b": ["c", "d"]}
        cls.result_test = [{"a": 0 , "b": "c"},
                           {"a": 0, "b": "d"},
                           {"a": 1 , "b": "c"},
                           {"a": 1 , "b": "d"}]

    def test_get_params_list(self):
        assert script.get_params_list(self.dict_test) == self.result_test
