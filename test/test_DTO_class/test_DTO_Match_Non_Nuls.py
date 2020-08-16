from app.DTO_class import DTO_Match_Non_Nuls as script
from app.DAO_class.DAO_Match_Non_Nuls import MatchNonNulModel, StandingNonNulModel, ScoreNonNulModel
import datetime
import numpy as np



FakeHomeTeamInfo = StandingNonNulModel(**{'position': 2, 'nb_de_matchs': 10, 'nb_de_win': 0, 'nb_de_nul': 3,
                                          'nb_de_lose': 0, 'points': 0, 'buts_marques': 0, 'buts_encaisses': 0})

FakeAwayTeamInfo = StandingNonNulModel(**{'position': 12, 'nb_de_matchs': 10, 'nb_de_win': 0, 'nb_de_nul': 4,
                                          'nb_de_lose': 0, 'points': 0, 'buts_marques': 0, 'buts_encaisses': 0})

FakeScore = ScoreNonNulModel(**{'winner': "Test", 'nul_index__': 0, 'home_serie_nul_': 3, 'away_serie_nul_': 1})

FakeMatchNonNulModel = MatchNonNulModel(score=FakeScore,
                                        home_team_info=FakeHomeTeamInfo,
                                        away_team_info=FakeAwayTeamInfo,
                                        id=0, match_status=0, match_day=0, home_team_id=0, away_team_id=1, in_home_team_index__=False,
                                        utc_date=datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
                                        )




class TestMatchNonNulData:

    @classmethod
    def setup_method(cls):
        cls.match_non_nul_data_obj = script.MatchNonNulData(match_object=FakeMatchNonNulModel)
        cls.home_serie_attr = 3
        cls.away_serie_attr = 1
        cls.abs_dif_pos = 10
        cls.home_nul_prob = 0.3
        cls.away_nul_prob = 0.4
        cls.target = 0

    def test_to_array(self):
        data_array, data_target = self.match_non_nul_data_obj.to_array
        data_array_test = np.array([self.home_serie_attr, self.away_serie_attr, self.abs_dif_pos, self.home_nul_prob, self.away_nul_prob])
        assert data_array[0] == data_array_test[0]
        assert data_array[1] == data_array_test[1]
        assert data_array[2] == data_array_test[2]
        assert data_array[3] == data_array_test[3]
        assert data_array[4] == data_array_test[4]
        assert data_target == np.array(self.target)


    def test_to_dict(self):
        assert self.match_non_nul_data_obj.to_dict == self.match_non_nul_data_obj.__dict__






