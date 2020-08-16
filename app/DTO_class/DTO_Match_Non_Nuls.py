from app.DAO_functions import CRUD_functions as Crud
from app.DTO_Parser_class.ParseClassModel import ParseBaseModel
from app.DTO_Parser_class.Decorateur_class_models.ParserMatchNonNulDecorator import MatchNonNulDecorator
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel, MatchNonNulModel
import pandas as pd
import numpy as np


class MatchNonNulData:
    """classe définissant un objet match non nul qui pourra être utilisé pour entrainer un model de machine learning

        attributs:
            - target (nul_index__)
            - home_serie_nul (match.score.home_serie_nul)
            - away_serie_nul (match.score.away_serie_nul)
            - diference de position entre les équipes: val_abs(home_team_position - away_team_position) (team.standing.position)
            - proportion de matchs nul team_nb_de_nul/team_nb_de_matchs pour les deux équipes (team.standing.nb_de_nul/team.standing.nb_de_nul)
    """


    def __init__(self, match_object: MatchNonNulModel):

        self.target = match_object.score.nul_index__

        self.home_serie = match_object.score.home_serie_nul_
        self.away_serie = match_object.score.away_serie_nul_
        self.abs_dif_pos = abs(match_object.home_team_info.position - match_object.away_team_info.position)
        self.home_nul_prob = round(match_object.home_team_info.nb_de_nul/match_object.home_team_info.nb_de_matchs, 5)
        self.away_nul_prob = round(match_object.away_team_info.nb_de_nul/match_object.away_team_info.nb_de_matchs, 5)


    @property
    def to_array(self):
        data_list = [self.home_serie, self.away_serie, self.abs_dif_pos, self.home_nul_prob, self.away_nul_prob]
        ret_data_array = np.array(data_list)
        ret_target_array = np.array(self.target)
        return ret_data_array, ret_target_array


    @property
    def to_dict(self):
        data_dict = self.__dict__
        return data_dict



class CompNonNulsDataModel(ParseBaseModel):  # pragma: no cover
    """classe regroupant toute la data pour une instance de CompNonNulModel
        l'usage du decorateur @MatchNonNulDecorateur permet l'acces a l'attribut 'parsed_comp_model__' qui contient la
        data parsé du comp_model

        cette data sera traitée par la fonction export_to_array pour pouvoir être traitée par un model de machine learning"""

    __match_data_model = MatchNonNulData

    def __init__(self, comp_id):
        super().__init__(comp_id)
        self.comp_model__ = CompNonNulModel.parse_obj(Crud.select_comp(self.comp_id))



    @MatchNonNulDecorator
    def export_to_array(self):
        match_list = self.parsed_comp_model__.matches_
        data_list = []
        target_list = []
        for match in match_list:
            data, target = self.__match_data_model(match).to_array
            data_list.append(data)
            target_list.append(target)

        ret_data_array = np.array(data_list)
        ret_target_array = np.array(target_list)
        return ret_data_array, ret_target_array


    @MatchNonNulDecorator
    def export_to_list(self):
        match_list = self.parsed_comp_model__.matches_
        data_list = []
        target_list = []
        for match in match_list:
            data, target = self.__match_data_model(match).to_array
            data_list.append(data)
            target_list.append(target)

        return data_list, target_list


    @MatchNonNulDecorator
    def export_to_dataframe(self):
        match_list = self.parsed_comp_model__.matches_
        dict_list = []
        for match in match_list:
            match_dict = self.__match_data_model(match).to_dict
            dict_list.append(match_dict)

        df = pd.DataFrame(dict_list)
        return df











