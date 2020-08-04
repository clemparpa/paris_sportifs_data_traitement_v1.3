from pydantic import BaseModel, constr
from typing import List, Any
import datetime




class FDMScoreModel(BaseModel):


    winner: Any
    half_time_home_score: Any
    full_time_home_score: Any
    full_time_away_score: Any
    half_time_away_score: Any


class FDMMatchModel(BaseModel):

    id: int
    match_status: constr(max_length=30)
    match_day: int
    utc_date: datetime.datetime
    home_team_id: int
    away_team_id: int

    score: FDMScoreModel



class FDMStandingModel(BaseModel):


    position: int
    nb_de_matchs: int
    nb_de_win: int
    nb_de_nul: int
    nb_de_lose: int
    points: int
    buts_marques: int
    buts_encaisses: int




class FDMTeamModel(BaseModel):

    id: int
    season_year: int


    standing: FDMStandingModel
    played_as_home_matches: List[FDMMatchModel]
    played_as_away_matches: List[FDMMatchModel]



class FDMCompModel(BaseModel):


    id: int


    teams: List[FDMTeamModel]



