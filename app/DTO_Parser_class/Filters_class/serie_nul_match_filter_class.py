from typing import List
from app.DAO_class.DAO_Match_Non_Nuls import MatchNonNulModel
from app.DTO_Parser_class.Filters_class.Abstract_filter_class import AbstractCompModelFilter
import operator


class ImplementSerieNulMatchFilter(AbstractCompModelFilter):
    """class contenant la fonction de filtre et le validateur
        pour parser le comp_model de façon à retirer les matchs non finis"""

    def __init__(self, comp_model):
        super().__init__(comp_model)


    def filter(self):

        def team_match_parser(team_model):


            copied_team_model = team_model.copy()
            match_team_list: List = copied_team_model.played_as_home_matches + copied_team_model.played_as_away_matches
            match_team_list.sort(key=operator.attrgetter('utc_date'))

            def match_filter(match_model: MatchNonNulModel, value):
                retour_match = match_model.copy()
                if match_model.in_home_team_index__:
                    retour_match.score.home_serie_nul_ = value
                    retour_match.score.away_serie_nul_ = 0
                else:
                    retour_match.score.away_serie_nul_ = value
                    retour_match.score.home_serie_nul_ = 0
                return retour_match


            #traitement des matchs

            last_match = None
            for match in match_team_list:
                if match == match_team_list[0]:
                    match = match_filter(match, 0)



                else:
                    if last_match.score.nul_index__ == 1:
                        match = match_filter(match, (last_match.score.home_serie_nul_ + last_match.score.away_serie_nul_ + 1))


                    elif last_match.score.nul_index__ == 0:
                        match = match_filter(match, 0)

                    else:
                        raise ValueError(f"le nul_index__ du match {last_match.id}, n'est ni 1 ni 0")


                last_match = match


            ret_team_model_dict = {
                "season_year": team_model.season_year,
                "standing": team_model.standing,
                "id": team_model.id,
                "played_as_home_matches": team_model.played_as_home_matches,
                "played_as_away_matches": team_model.played_as_away_matches,
                "match_list_": match_team_list
            }

            ret_team_model = team_model.__class__(**ret_team_model_dict)
            return ret_team_model

        ret_comp_model_dict = {
            "id": self.comp_model.id,
            "teams": list(map(team_match_parser, self.comp_model.teams)),
        }

        ret_comp_model = self.comp_model.__class__(**ret_comp_model_dict)
        self.comp_model = ret_comp_model


    def validator(self):


        def sort_validator():


            error_team_list = []
            for team in self.comp_model.teams:
                if team.match_list_:
                    if team.match_list_ != sorted(team.match_list_, key=operator.attrgetter('utc_date')):
                        error_team_list.append(team)
                else:
                    raise ValueError(f"l'attribut 'match_list_', implémentant la liste des matchs d'une équipe n'est pas renseigné pour l'équipe {team.id} "
                                     f"erreur critique")


            total_error = ""
            if len(error_team_list) > 0:
                home_error = ""
                for team in error_team_list:
                    str_error = f" SortValidatorError: la team {team.played_as_home_matches[0].home_team_id} a ses matchs qui n'ont pas été triés par le filter \n"
                    home_error += str_error
                total_error += home_error

            if total_error != "":
                raise ValueError(total_error)


        def serie_validator():

            total_error = ""
            for team in self.comp_model.teams:


                match_list_ = team.match_list_


                match_error_list = []
                last_match = None
                for match in match_list_:
                    if match == match_list_[0]:
                        if match.score.home_serie_nul_ + match.score.away_serie_nul_ != 0:
                            match_error_list.append(match)

                    else:
                        if last_match.score.nul_index__ == 1:
                            if (match.score.home_serie_nul_ + match.score.away_serie_nul_) != (last_match.score.home_serie_nul_ + last_match.score.away_serie_nul_ + 1):
                                match_error_list.append(match)

                        elif last_match.score.nul_index__ == 0:
                            if (match.score.home_serie_nul_ + match.score.away_serie_nul_) != 0:
                                match_error_list.append(match)

                    if match.score.home_serie_nul_ != 0 and match.score.away_serie_nul_ != 0:
                        match_error_list.append(match)

                    last_match = match

                team_str_errors = ""
                if len(match_error_list) > 0:
                    for match in match_error_list:
                        str_error = f"Serie Validator Error: le match {match.id} a ses séries de nuls (home: {match.score.home_serie_nul_}, away: {match.score.away_serie_nul_}) erronées \n"
                        team_str_errors += str_error

                total_error += team_str_errors


            if total_error != "":
                raise ValueError(total_error)


        sort_validator()
        serie_validator()



