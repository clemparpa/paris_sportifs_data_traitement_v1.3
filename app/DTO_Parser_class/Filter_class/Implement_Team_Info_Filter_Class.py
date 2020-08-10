from app.DTO_Parser_class.Filter_class.Filter_Main_Class import CompModelMainFilter
from typing import List


class ImplementTeamInfoCompModelFilter(CompModelMainFilter):


    class TeamFilter(CompModelMainFilter.TeamFilter):

        def team_filter(self, home_match_list: List = None, away_match_list: List = None,
                        total_match_list: List = None) -> dict:
            ret_home_match_list = []
            ret_away_match_list = []
            for match in home_match_list:
                ret_match = match.copy(update={"home_team_info": self.team.standing})
                ret_home_match_list.append(ret_match)

            for match in away_match_list:
                ret_match = match.copy(update={"away_team_info": self.team.standing})
                ret_away_match_list.append(ret_match)


            return {"played_as_home_matches": ret_home_match_list, "played_as_away_matches": ret_away_match_list}



    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):
        return super().filter(all_matches=False, sort_matches=False, sort_key=None)

