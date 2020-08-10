import operator

from app.DTO_Parser_class.Filter_class import Filter_Main_Class as script
from app.DAO_class.DAO_FineDataModel import FDMCompModel
from app.DAO_functions import CRUD_functions as Crud
import pytest



class TestCompModelFilter:

    @classmethod
    def setup_method(cls):
        comp_model = FDMCompModel.parse_obj(Crud.select_comp(2021))
        cls.comp_filter_object = script.CompModelMainFilter(comp_model)


    def test_filter_args_exception_raiser(self):
        with pytest.raises(AttributeError):
            self.comp_filter_object.filter(sort_matches=False, sort_key="random_string")

        with pytest.raises(AttributeError):
            self.comp_filter_object.filter(sort_matches=True)


    def test_filter_separed_match_no_sort(self):
        comp_model_before = self.comp_filter_object.comp_model.copy()
        self.comp_filter_object.filter(all_matches=False, sort_matches=False, sort_key=None)
        assert comp_model_before == self.comp_filter_object.comp_model


    def test_filter_separed_match_sort(self):
        comp_model_before = self.comp_filter_object.comp_model.copy()
        for team in comp_model_before.teams:
            team.played_as_home_matches.sort(key=operator.attrgetter("utc_date"))
            team.played_as_away_matches.sort(key=operator.attrgetter("utc_date"))
        self.comp_filter_object.filter(all_matches=False, sort_matches=True, sort_key="utc_date")
        assert comp_model_before == self.comp_filter_object.comp_model


    def test_filter_all_match_no_sort(self):
        comp_model_before = self.comp_filter_object.comp_model.copy()

        self.comp_filter_object.filter(all_matches=True, sort_matches=False, sort_key=None)
        for team_before, team_after in zip(comp_model_before.teams, self.comp_filter_object.comp_model.teams):
            assert (team_before.played_as_home_matches + team_before.played_as_away_matches) == team_after.match_list_


    def test_filter_all_match_sort(self):
        comp_model_before = self.comp_filter_object.comp_model.copy()
        self.comp_filter_object.filter(all_matches=True, sort_matches=True, sort_key="utc_date")

        for team_before, team_after in zip(comp_model_before.teams, self.comp_filter_object.comp_model.teams):
            assert (sorted(team_before.played_as_home_matches + team_before.played_as_away_matches, key=operator.attrgetter("utc_date"))) == team_after.match_list_

