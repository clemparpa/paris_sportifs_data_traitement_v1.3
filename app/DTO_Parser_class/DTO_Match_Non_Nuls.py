from app.DAO_class import DAO_Match_Non_Nuls as dao

from app.DAO_functions import CRUD_functions as Crud
from app.DTO_Parser_class.ParseClassModel import ParseBaseModel
from app.DTO_Parser_class.Decorateur_class_models.ParserMatchNonNulDecorator import MatchNonNulDecorator
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel
import operator




class CompNonNulsParsedModel(ParseBaseModel):
    """classe regroupant toute la data pour une instance de l'application MatchNonNuls"""

    __comp_model__ = CompNonNulModel.parse_obj(Crud.select_comp(2021))



    @MatchNonNulDecorator
    def test(self):
        match_list = []
        for teams in self.__comp_model__.teams:
            matchs = teams.played_as_away_matches + teams.played_as_home_matches
            match_list.extend(matchs)

        for els in match_list:
            if els.match_status != 'FINISHED':
                print(els)



    @MatchNonNulDecorator
    def autre_test(self):
        match_list = sorted((self.__parsed_comp_model__.teams[2].played_as_away_matches + self.__parsed_comp_model__.teams[2].played_as_home_matches), key=operator.attrgetter("utc_date"))


        for n in range(20):
            print(match_list[n].in_home_team_index__, "  ", match_list[n].score, "  :  ", match_list[n].utc_date)



    @MatchNonNulDecorator
    def test_test(self):
        for match in self.__parsed_comp_model__.matches_:
            print(match)

        print(len(self.__parsed_comp_model__.matches_))



CompNonNulsParsedModel.test_test()
