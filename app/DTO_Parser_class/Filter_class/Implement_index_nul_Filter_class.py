from app.DTO_Parser_class.Filter_class.Filter_Main_Class import CompModelMainFilter



class ImplementIndexNulCompModelFilter(CompModelMainFilter):


    class MatchFilter(CompModelMainFilter.MatchFilter):


        def match_home_filter(self) -> dict:
            if self.match.score.winner == "DRAW":
                return {"score": self.match.score.copy(update={"nul_index__": 1})}

            else:
                return {"score": self.match.score.copy(update={"nul_index__": 0})}


        def match_away_filter(self) -> dict:
            if self.match.score.winner == "DRAW":
                return {"score": self.match.score.copy(update={"nul_index__": 1})}

            else:
                return {"score": self.match.score.copy(update={"nul_index__": 0})}


    def filter(self, all_matches: bool = False, sort_matches: bool = False, sort_key: str = None):
        return super().filter(all_matches=False, sort_matches=False, sort_key=None)
