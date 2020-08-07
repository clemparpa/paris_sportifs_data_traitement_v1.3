from app.DTO_Parser_class.Filters_class_depracated.Abstract_filter_class import AbstractCompModelFilter



class ImplementHomeTeamIndexFilter(AbstractCompModelFilter):
    """class contenant la fonction de filtre et le validateur
        pour parser le comp_model de façon à implementer les attributs 'in_home_team_index__' de chaque match_model"""

    def __init__(self, comp_model):
        super().__init__(comp_model)


    def filter(self):

        def team_match_parser(team_model):

            def away_match_filter(match_model):
                match_model.in_home_team_index__ = False
                return match_model

            def home_match_filter(match_model):
                match_model.in_home_team_index__ = True
                return match_model

            ret_team_model_dict = {
                "season_year": team_model.season_year,
                "standing": team_model.standing,
                "id": team_model.id,
                "played_as_home_matches": list(filter(home_match_filter, team_model.played_as_home_matches)),
                "played_as_away_matches": list(filter(away_match_filter, team_model.played_as_away_matches)),
            }

            ret_team_model = team_model.__class__(**ret_team_model_dict)
            return ret_team_model

        ret_comp_model_dict = {
            "teams": list(map(team_match_parser, self.comp_model.teams)),
        }

        self.comp_model = self.comp_model.copy(update=ret_comp_model_dict)


    def validator(self):

        error_list = []
        for team in self.comp_model.teams:
            home_matchs = team.played_as_home_matches
            away_matchs = team.played_as_away_matches

            for match in home_matchs:
                if not match.in_home_team_index__:
                    error_list.append(match)

            for match in away_matchs:
                if match.in_home_team_index__:
                    error_list.append(match)


        if len(error_list) > 0:
            return_error = ""
            for match in error_list:
                str_error = f"le match {match.id}, opposant les équipes {match.home_team_id}, {match.away_team_id}, " \
                            f"a pour in_home_team_index__ {match.in_home_team_index__} ce qui est éroné\n"
                return_error += str_error

            raise ValueError(return_error)




