from app.DAO_class.DAO_FineDataModel import FDMCompModel
from abc import ABC, abstractmethod
import operator
from typing import List
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel
from app.DAO_functions import CRUD_functions as Crud


class CompModelFilter:
    """classe abstraite définissant un filtre a appliquer a un comp_model
        le filtre est suivi d'une fonction validator() qui vérifie le parsing effectuée par le filtre
        l'étape de parsing et de validation avec le retour du comp_model est assurée par la fonction
        qui ne sera par override get_filtered_and_validated()

        pour l'overriding de la methode abstraite filter():
        -si une fonction 'team_match_parser()' est définie:
            on définit un dictionnaire de team_model a renvoyer que l'on renvoit avec le snippet suivant afin de pallier
            les problemes de classe de l'objet team_model, car ainsi le 'ret_team_model' renvoyé sera de la meme classe que le 'team_model'
            passé en attribut de la fonction 'team_match_parser()':

            ------------------------------------------------------------
            ret_team_model = team_model.__class__(**ret_team_model_dict)
            return ret_team_model
            ------------------------------------------------------------
        -de la meme façon l'attribution du nouveau comp_model de la fonction filter sera effectué grace au snippet suivant pour éviter les problemes
            liés a la classe du comp_model:

            ------------------------------------------------------------
            ret_comp_model = self.comp_model.__class__(**ret_comp_model_dict)
            self.comp_model = ret_comp_model
            ------------------------------------------------------------
    """

    def __init__(self, comp_model):
        self.comp_model = comp_model



    class MatchFilter:

        def __init__(self, match_object):
            self.match = match_object

        def match_total_filter(self) -> dict:
            return self.match.dict()

        def match_home_filter(self) -> dict:
            return self.match.dict()

        def match_away_filter(self) -> dict:
            return self.match.dict()

        def apply_match_total_filter(self):
            match_obj = self.match.copy(update=self.match_total_filter())
            return match_obj

        def apply_match_home_filter(self):
            match_obj = self.match.copy(update=self.match_home_filter())
            return match_obj

        def apply_match_away_filter(self):
            match_obj = self.match.copy(update=self.match_away_filter())
            return match_obj



    class TeamFilter:

        def __init__(self, team_obj):
            self.team = team_obj

        def team_filter(self, home_match_list: List = None, away_match_list: List = None, total_match_list: List = None) -> dict:
            return self.team.dict()

        def apply_team_filter(self, home_match_list: List = None, away_match_list: List = None, total_match_list: List = None):
            team_obj = self.team.copy(update=self.team_filter(home_match_list, away_match_list, total_match_list))
            return team_obj


    class CompFilter:

        def __init__(self, comp_obj):
            self.comp = comp_obj

        def comp_filter(self, team_list: List = None):
            return self.comp.dict()

        def apply_comp_filter(self, team_list: List = None):
            comp_obj = self.comp.copy(update=self.comp_filter(team_list=team_list))
            return comp_obj



    @staticmethod
    def check_filter_args(sort_matches: bool, sort_key: str):

        if sort_matches is True and sort_key is None:
            raise AttributeError(
                f"le filtre appelé a des arguments incorrect: l'argument 'sort_matches' vaut {sort_matches} "
                f"mais l'argument, nécessaire vaut {sort_key} veuillez renseigner l'argument 'sort_key' "
                f"ou passer l'argument 'sort_matches' a 'False'")

        if sort_matches is False and sort_key is not None:
            raise AttributeError(
                f"le filtre appelé a des arguments incorrect: l'argument 'sort_matches' vaut {sort_matches} "
                f"mais l'argument 'sort_key' valant {sort_key} est défini. Veuillez passer l'argument"
                f" 'sort_matches' a 'True' pour que le tri soit effectué ou passer l'argument 'sort_key' "
                f"a 'None' pour que le tri ne soit pas effectué")



    @staticmethod
    def implement_match_list(team_obj, all_matches: bool, sort_matches: bool, sort_key: str) -> tuple:
        if all_matches:
            if sort_matches:
                match_total_list = sorted((team_obj.played_as_home_matches + team_obj.played_as_away_matches),
                                          key=operator.attrgetter(sort_key))

            else:
                match_total_list = team_obj.played_as_home_matches + team_obj.played_as_away_matches

            ret_match_list = (match_total_list,)
            return ret_match_list

        else:
            if sort_matches:
                home_match_list = sorted(team_obj.played_as_home_matches, key=operator.attrgetter(sort_key))
                away_match_list = sorted(team_obj.played_as_away_matches, key=operator.attrgetter(sort_key))

            else:
                home_match_list = team_obj.played_as_home_matches
                away_match_list = team_obj.played_as_away_matches

            ret_match_list = (home_match_list, away_match_list,)
            return ret_match_list



    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):

        self.check_filter_args(sort_matches=sort_matches, sort_key=sort_key)

        updated_team_list = []
        for team in self.comp_model.teams:

            match_list_tuple = self.implement_match_list(team_obj=team, all_matches=all_matches,
                                                         sort_matches=sort_matches, sort_key=sort_key)

            if len(match_list_tuple) == 1:

                updated_match_list = []
                for match in match_list_tuple[0]:
                    updated_match = self.MatchFilter(match_object=match).apply_match_total_filter()
                    updated_match_list.append(updated_match)

                updated_team = self.TeamFilter(team_obj=team).apply_team_filter(total_match_list=updated_match_list)
                updated_team_list.append(updated_team)


            elif len(match_list_tuple) == 2:

                updated_home_match_list = []
                updated_away_match_list = []
                for match in match_list_tuple[0]:
                    updated_match = self.MatchFilter(match_object=match).apply_match_home_filter()
                    updated_home_match_list.append(updated_match)

                for match in match_list_tuple[1]:
                    updated_match = self.MatchFilter(match_object=match).apply_match_away_filter()
                    updated_away_match_list.append(updated_match)

                updated_team = self.TeamFilter(team_obj=team).apply_team_filter(home_match_list=updated_home_match_list,
                                                                                away_match_list=updated_away_match_list)
                updated_team_list.append(updated_team)


            updated_comp = self.CompFilter(comp_obj=self.comp_model).apply_comp_filter(team_list=updated_team_list)
            self.comp_model = updated_comp



"""
comp_model__ = CompNonNulModel.parse_obj(Crud.select_comp(2021))
a = CompModelFilter(comp_model__)
print(a.comp_model.dict())

a.filter()
for team in a.comp_model.teams:
    print(team)
"""