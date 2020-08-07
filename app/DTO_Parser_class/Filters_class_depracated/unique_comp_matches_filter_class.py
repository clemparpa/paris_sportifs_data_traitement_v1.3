from app.DTO_Parser_class.Filters_class_depracated.Abstract_filter_class import AbstractCompModelFilter
import operator


class ImplementCompModelMatches(AbstractCompModelFilter):
    """class contenant la fonction de filtre et le validateur
        pour parser le comp_model de façon à implémenter l'attribut 'matches_' de comp_model"""

    def __init__(self, comp_model):
        super().__init__(comp_model)

    def filter(self):

        matches = []
        uniques_matches = []
        for team in self.comp_model.teams:
            print(team.match_list_)
            matches.extend(team.match_list_)


        matches.sort(key=operator.attrgetter("id"))
        # tuples
        tuples_matches = []
        for idx, elt in enumerate(matches[:len(matches) - 1]):
            if idx % 2 == 0:
                tuples_matches.append((matches[idx], matches[idx + 1],))


        for paire_match in tuples_matches:
            if paire_match[0].id == paire_match[1].id:
                new_match = paire_match[0].copy()
                new_match.score.home_serie_nul_ += paire_match[1].score.home_serie_nul_
                new_match.score.away_serie_nul_ += paire_match[1].score.away_serie_nul_

                if new_match.home_team_info is None:
                    new_match.home_team_info = paire_match[1].home_team_info


                if new_match.away_team_info is None:
                    new_match.away_team_info = paire_match[1].away_team_info

                uniques_matches.append(new_match)

            else:
                raise ValueError(
                    f"le tri n'a pas été effectué les id {paire_match[0].id} et {paire_match[1].id} ne sont pas égales")



        ret_comp_model_dict = {
            "matches_": uniques_matches
        }


        self.comp_model = self.comp_model.copy(update=ret_comp_model_dict)

    def validator(self):


        if not self.comp_model.matches_:
            raise ValueError("le filtre a été mal appliqué l'attribut 'comp_mode.matches_' n'est pas implémenté")

        else:
            error_list = []
            sorted_matches = sorted(self.comp_model.matches_, key=operator.attrgetter("id"))
            last_match = None
            for match in sorted_matches:
                if match != sorted_matches[0]:
                    if match.id == last_match.id:
                        error_list.append((last_match, match))

                last_match = match

            if len(error_list) > 0:
                return_error = ""
                for match_pair in error_list:
                    str_error = f"le match {match_pair[0].id}, {match_pair[1].id} est en deux exemplaire  \n"
                    return_error += str_error

                raise ValueError(return_error)
