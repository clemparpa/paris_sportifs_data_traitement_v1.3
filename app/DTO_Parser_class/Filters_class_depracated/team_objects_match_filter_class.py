from app.DTO_Parser_class.Filters_class_depracated.Abstract_filter_class import AbstractCompModelFilter


class ImplementTeamObjectsMatchFilter(AbstractCompModelFilter):

    def __init__(self, comp_model):
        super().__init__(comp_model)

    def filter(self):

        def team_match_parser(team_model):

            team_cpy = team_model.copy()

            for match in team_cpy.played_as_home_matches:
                if hasattr(match, "home_team_info"):
                    match.home_team_info = team_cpy.standing
                    match.away_team_info = None

                else:
                    raise AttributeError(f"Fatal Error: le match {match.id} ne possede pas d'attribut 'home_team_model' "
                                         f"ce qui devrait être le cas le comp_model utilisé devrait être le model "
                                         "'CompModelNonNul' ce qui n'est peut être pas le cas")

            for match in team_cpy.played_as_away_matches:
                if hasattr(match, "away_team_info"):
                    match.away_team_info = team_cpy.standing
                    match.home_team_info = None

                else:
                    raise AttributeError(
                        f"Fatal Error: le match {match.id} ne possede pas d'attribut 'away_team_model' "
                        f"ce qui devrait être le cas le comp_model utilisé devrait être le model "
                        "'CompModelNonNul' ce qui n'est peut être pas le cas")


            ret_team_model_dict = {
                "season_year": team_model.season_year,
                "standing": team_model.standing,
                "id": team_model.id,
                "played_as_home_matches": team_cpy.played_as_home_matches,
                "played_as_away_matches": team_cpy.played_as_away_matches,
            }

            ret_team_model = team_model.__class__(**ret_team_model_dict)
            return ret_team_model

        ret_comp_model_dict = {
            "teams": list(map(team_match_parser, self.comp_model.teams)),
        }

        self.comp_model = self.comp_model.copy(update=ret_comp_model_dict)


    def validator(self):
        match_list = []

        for team in self.comp_model.teams:
            match_team_list = team.played_as_home_matches + team.played_as_away_matches
            match_list.extend(match_team_list)

        error_list = []
        for match in match_list:
            if match.away_team_info is None and match.home_team_info is None:
                error_list.append(match)


        if len(error_list) > 0:
            return_error = ""
            for match in error_list:
                str_error = f"le match {match.id}, opposant les équipes {match.home_team_id}, {match.away_team_id}, ne possède pas " \
                            f"de valeurs dans ses attributs away_team_info et home_team_info alors que le filtre devait " \
                            f"lui en fournir: voila les valeurs '{match.home_team_info}', '{match.away_team_info}' " \

                return_error += str_error

            raise ValueError(return_error)






