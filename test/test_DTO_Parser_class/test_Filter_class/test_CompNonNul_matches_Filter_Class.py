import operator
from app.DTO_Parser_class.ParseClassModel import ParseBaseModel
from app.DTO_Parser_class.Decorateur_class_models.ParserMatchNonNulDecorator import MatchNonNulDecorator
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel
from app.DAO_functions import CRUD_functions as Crud
from app.DAO_class.DAO_Match_Non_Nuls import StandingNonNulModel



class FakeDecoredData(ParseBaseModel):

    def __init__(self, comp_id):
        super().__init__(comp_id)
        self.comp_model__ = CompNonNulModel.parse_obj(Crud.select_comp(self.comp_id))


    @MatchNonNulDecorator
    def test_global_filter(self):
        pass




class TestImplementCompNonNulMatchesFilter:

    @classmethod
    def setup_method(cls):
        cls.comp_filter_object = FakeDecoredData(2021)
        cls.comp_filter_object.test_global_filter()


    def test_finished_matches(self):

        for teams in self.comp_filter_object.parsed_comp_model__.teams:

            for match in teams.played_as_home_matches:
                assert match.match_status == 'FINISHED'

            for match in teams.played_as_away_matches:
                assert match.match_status == 'FINISHED'


    def test_index_nul_(self):
        comp_match_list = []
        for teams in self.comp_filter_object.parsed_comp_model__.teams:
            match_list = teams.played_as_home_matches + teams.played_as_away_matches
            comp_match_list.extend(match_list)


        for match in comp_match_list:
            if match.score.winner == "DRAW":
                assert match.score.nul_index__ == 1

            else:
                assert match.score.nul_index__ == 0


    def test_in_home_team_index(self):

        for teams in self.comp_filter_object.parsed_comp_model__.teams:

            for match in teams.played_as_home_matches:
                assert match.in_home_team_index__ is True

            for match in teams.played_as_away_matches:
                assert match.in_home_team_index__ is False


    def test_team_info(self):

        for teams in self.comp_filter_object.parsed_comp_model__.teams:

            for match in teams.played_as_home_matches:
                assert match.home_team_info == teams.standing

            for match in teams.played_as_away_matches:
                assert match.away_team_info == teams.standing


    def test_team_serie_index(self):

        for teams in self.comp_filter_object.parsed_comp_model__.teams:

            assert teams.match_list_ == sorted((teams.played_as_home_matches + teams.played_as_away_matches), key=operator.attrgetter("utc_date"))

            last_match = None
            for match in teams.match_list_:

                assert match.score.home_serie_nul_ != -1 or match.score.away_serie_nul_ != -1

                if match == teams.match_list_[0]:
                    if match.in_home_team_index__:
                        assert match.score.home_serie_nul_ == 0
                    else:
                        assert match.score.away_serie_nul_ == 0

                else:
                    if last_match.score.nul_index__ == 0:
                        if match.in_home_team_index__:
                            assert match.score.home_serie_nul_ == 0
                        else:
                            assert match.score.away_serie_nul_ == 0

                    elif last_match.score.nul_index__ == 1:
                        if last_match.in_home_team_index__:
                            if match.in_home_team_index__:
                                assert match.score.home_serie_nul_ == last_match.score.home_serie_nul_ + 1
                            else:
                                assert match.score.away_serie_nul_ == last_match.score.home_serie_nul_ + 1

                        else:
                            if match.in_home_team_index__:
                                assert match.score.home_serie_nul_ == last_match.score.away_serie_nul_ + 1
                            else:
                                assert match.score.away_serie_nul_ == last_match.score.away_serie_nul_ + 1



                last_match = match



    def test_unique_match_list(self):

        for match in self.comp_filter_object.parsed_comp_model__.matches_:

            assert type(match.home_team_info) == StandingNonNulModel
            assert type(match.away_team_info) == StandingNonNulModel


