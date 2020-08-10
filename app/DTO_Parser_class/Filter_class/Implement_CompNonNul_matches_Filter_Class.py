import operator
from app.DTO_Parser_class.Filter_class.Filter_Main_Class import CompModelMainFilter
from typing import List


class ImplementMatchesCompModelFilter(CompModelMainFilter):


    class CompFilter(CompModelMainFilter.CompFilter):

        def comp_filter(self, team_list: List = None) -> dict:

            doble_match_list = []
            for team in team_list:
                doble_match_list.extend(team.match_list_)


            doble_match_list.sort(key=operator.attrgetter("id"))

            tuple_match_list = []
            tuple_error_list = []
            for index, match in enumerate(doble_match_list):
                if index % 2 == 0:
                    if match.id == doble_match_list[index + 1].id:
                        tuple_match_list.append((match, doble_match_list[index + 1]))

                    else:
                        tuple_error_list.append((match, doble_match_list[index + 1]))  # pragma: no cover


            str_error = ""  # pragma: no cover
            for tuples in tuple_error_list: # pragma: no cover
                error = f"le doublon est éronné les ids '{tuples[0].id} et {tuples[1].id}\n' " # pragma:  no cover
                str_error += error  # pragma: no cover

            if str_error != "":  # pragma: no cover
                raise ValueError(str_error)  # pragma: no cover


            ret_match_list = []
            for tuples in tuple_match_list:
                match_cpy = tuples[0].copy()
                if tuples[0].in_home_team_index__ and not tuples[1].in_home_team_index__:
                    match_cpy.score.away_serie_nul_ = tuples[1].score.away_serie_nul_
                    match_cpy.away_team_info = tuples[1].away_team_info

                elif not tuples[0].in_home_team_index__ and tuples[1].in_home_team_index__:
                    match_cpy.score.home_serie_nul_ = tuples[1].score.home_serie_nul_
                    match_cpy.home_team_info = tuples[1].home_team_info

                ret_match_list.append(match_cpy)


            return {"matches_": ret_match_list}



    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):
        return super().filter(all_matches=False, sort_matches=False, sort_key=None)






