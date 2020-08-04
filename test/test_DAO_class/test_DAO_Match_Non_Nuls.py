from app.DAO_class import DAO_Match_Non_Nuls as script
from app.DAO_functions import CRUD_functions as Crud






class TestDAOMatchNonNuls:

    @classmethod
    def setup_class(cls):
        data = Crud.select_comp(2019)
        cls.comp_model_for_test = script.CompNonNulModel.parse_obj(data.dict())



    def test_model_comp(self):

        assert self.comp_model_for_test.id == 2019


    def test_model_teams(self):
        assert type(self.comp_model_for_test.teams) == list
        assert type(self.comp_model_for_test.teams[0].played_as_away_matches) == list
        assert type(self.comp_model_for_test.teams[0].played_as_home_matches) == list


