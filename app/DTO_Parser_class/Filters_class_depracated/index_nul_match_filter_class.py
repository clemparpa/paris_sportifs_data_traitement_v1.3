from app.DTO_Parser_class.Filters_class_depracated.Abstract_filter_class import AbstractCompModelFilter



class ImplementIndexNulMatchFilter(AbstractCompModelFilter):


    def __init__(self, comp_model):
        super().__init__(comp_model)


    def filter(self):

        def team_match_parser(team_model):


            def match_filter(match_model):
                if hasattr(match_model.score, "nul_index__"):
                    if match_model.score.winner == 'DRAW':
                        match_model.score.nul_index__ = 1
                else:
                    raise AttributeError("le match_model passé dans la fonction match_filter du filtre ne contient pas "
                                         "d'attribut 'nul_index__' le comp_model utilisé devrait être le model "
                                         "'CompModelNonNul' ce qui n'est peut être pas le cas")

                return match_model


            ret_team_model_dict = {
                "season_year": team_model.season_year,
                "standing": team_model.standing,
                "id": team_model.id,
                "played_as_home_matches": list(filter(match_filter, team_model.played_as_home_matches)),
                "played_as_away_matches": list(filter(match_filter, team_model.played_as_away_matches)),
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
            if match.score.winner == 'DRAW':
                if match.score.nul_index__ != 1:
                    error_list.append(match)

            elif match.score.winner != 'DRAW':
                if match.score.nul_index__ != 0:
                    error_list.append(match)
                    
                    
                
        if len(error_list) > 0:
            return_error = ""
            for match in error_list:
                str_error = f"le match {match.id}, opposant les équipes {match.home_team_id}, {match.away_team_id}, est une {match.score.winner} " \
                            f"mais son nul_index__ vaut {match.score.nul_index__} alors que celui_ci devrait valoir 1 \n"
                return_error += str_error

            raise ValueError(return_error)






