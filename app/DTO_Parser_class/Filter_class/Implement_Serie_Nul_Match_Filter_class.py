from app.DTO_Parser_class.Filter_class.Filter_Main_Class import CompModelMainFilter
from typing import List


class ImplementSerieNulCompModelFilter(CompModelMainFilter):


    class TeamFilter(CompModelMainFilter.TeamFilter):


        def team_filter(self, home_match_list: List = None, away_match_list: List = None, total_match_list: List = None) -> dict:

            ret_match_list = []

            def match_filter(match_model, value):
                retour_match = match_model.copy()
                if match_model.in_home_team_index__:
                    retour_match.score.home_serie_nul_ = value
                    retour_match.score.away_serie_nul_ = -1
                else:
                    retour_match.score.away_serie_nul_ = value
                    retour_match.score.home_serie_nul_ = -1
                return retour_match



            last_match = None
            for match in total_match_list:

                if match == total_match_list[0]:
                    ret_match = match_filter(match, 0)
                    ret_match_list.append(ret_match)


                else:
                    if last_match.score.nul_index__ == 1:
                        if last_match.in_home_team_index__:
                            ret_match = match_filter(match, (last_match.score.home_serie_nul_ + 1))
                        else:
                            ret_match = match_filter(match, (last_match.score.away_serie_nul_ + 1))
                        ret_match_list.append(ret_match)


                    elif last_match.score.nul_index__ == 0:
                        ret_match = match_filter(match, 0)
                        ret_match_list.append(ret_match)

                last_match = match


            return {"match_list_": ret_match_list}



    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):
        return super().filter(all_matches=True, sort_matches=True, sort_key="utc_date")
































