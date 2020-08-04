from pydantic import BaseModel, constr
from typing import List, Any
import datetime




class ScoreNonNulModel(BaseModel):


    winner: Any
    nul_index__: int = 0
    home_serie_nul_: int = 0
    away_serie_nul_: int = 0


class MatchNonNulModel(BaseModel):

    id: int
    match_status: constr(max_length=30)
    match_day: int
    utc_date: datetime.datetime
    home_team_id: int
    away_team_id: int


    in_home_team_index__: bool = False


    score: ScoreNonNulModel



class StandingNonNulModel(BaseModel):


    position: int
    nb_de_matchs: int
    nb_de_win: int
    nb_de_nul: int
    nb_de_lose: int
    points: int
    buts_marques: int
    buts_encaisses: int




class TeamNonNulModel(BaseModel):

    id: int
    season_year: int


    standing: StandingNonNulModel
    played_as_home_matches: List[MatchNonNulModel]
    played_as_away_matches: List[MatchNonNulModel]
    match_list_: List = []



class CompNonNulModel(BaseModel):


    id: int


    teams: List[TeamNonNulModel]
    matches_: List = []




