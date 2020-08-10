from app.DTO_Parser_class.Filter_class.Filter_Main_Class import CompModelMainFilter


class ImplementInHomeTeamIndexCompModelFilter(CompModelMainFilter):


    class MatchFilter(CompModelMainFilter.MatchFilter):


        def match_home_filter(self) -> dict:
            return {"in_home_team_index__": True}


        def match_away_filter(self) -> dict:
            return {"in_home_team_index__": False}


    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):
        return super().filter(all_matches=False, sort_matches=False, sort_key=None)






