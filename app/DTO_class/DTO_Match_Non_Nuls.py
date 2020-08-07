from app.DAO_functions import CRUD_functions as Crud
from app.DTO_Parser_class.ParseClassModel import ParseBaseModel
from app.DTO_Parser_class.Decorateur_class_models.ParserMatchNonNulDecorator import MatchNonNulDecorator
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel
import operator
import numpy as np



class CompNonNulsParsedModel(ParseBaseModel):
    """classe regroupant toute la data pour une instance de CompNonNulModel
        l'usage du decorateur @MatchNonNulDecorateur permet l'acces a l'attribut 'parsed_comp_model__' qui contient la
        data parsé du comp_model

        cette data sera traitée par la fonction export_to_array pour pouvoir être traitée par un model de machine learning"""


    def __init__(self, comp_id):
        super().__init__(comp_id)
        self.comp_model__ = CompNonNulModel.parse_obj(Crud.select_comp(self.comp_id))



    @MatchNonNulDecorator
    def export_to_array(self):
        comp_model = self.parsed_comp_model__
        pass

    @MatchNonNulDecorator
    def test(self):
        pass
        #comp_model = self.parsed_comp_model__
        #for i in range(20):
        #print(comp_model.matches_[i])



class MatchNonNulData:
    """classe définissant un objet match non nul qui pourra être utilisé pour entrainer un model de machine learning

        attributs:
            - target (nul_index__)
            - home_serie_nul (match.score.home_serie_nul)
            - away_serie_nul (match.score.away_serie_nul)
            - diference de position entre les équipes: val_abs(home_team_position - away_team_position) (team.standing.position)
            - proportion de matchs nul team_nb_de_nul/team_nb_de_matchs pour les deux équipes (team.standing.nb_de_nul/team.standing.nb_de_nul)
    """


    def __init__(
            self, nul_index__, home_serie_nul, away_serie_nul, home_nb_nul, home_nb_match, away_nb_nul,
            away_nb_match, home_position, away_position):


        self.target = nul_index__
        self.home_serie = home_serie_nul
        self.away_serie = away_serie_nul
        self.abs_dif_pos = abs(home_position - away_position)
        self.home_nul_prob = round(home_nb_nul/home_nb_match, 5)
        self.away_nul_prob = round(away_nb_nul/away_nb_match, 5)


    def to_array(self):
        ret_array = np.array(list(self.__dict__.values()))
        return ret_array




CompNonNulsParsedModel(2021).test()

