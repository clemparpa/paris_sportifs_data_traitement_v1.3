from pydantic import BaseModel, constr, Field
from typing import List, Any
import datetime




class ScoreModel(BaseModel):

    id: int
    winner: Any
    duration: Any
    half_time_home_score: Any
    full_time_home_score: Any
    full_time_away_score: Any
    half_time_away_score: Any
    last_update: datetime.datetime

    class Config:
        orm_mode = True



class MatchModel(BaseModel):

    id: int
    match_status: constr(max_length=30)
    season_id: int
    season_year: int
    match_day: int
    comp_id: int
    utc_date: datetime.datetime
    home_team_id: int
    away_team_id: int
    last_update: datetime.datetime

    class Config:
        orm_mode = True

    score: ScoreModel = Field(alias="entity_score_match")



class StandingModel(BaseModel):

    id: int

    comp_id: int
    season_year: int
    FDO_team_id: int


    position: int
    team_name: constr(max_length=50)
    nb_de_matchs: int
    nb_de_win: int
    nb_de_nul: int
    nb_de_lose: int
    points: int
    buts_marques: int
    buts_encaisses: int


    class Config:
        orm_mode = True



class TeamModel(BaseModel):

    id: int

    comp_id: int
    season_year: int
    FDO_team_id: int


    team_name: constr(max_length=100)
    team_area: Any
    team_short_name: constr(max_length=30)
    team_tla: Any
    founded: Any
    venue: Any
    club_colors: Any
    last_update: datetime.datetime

    standing: StandingModel = Field(alias="entity_standing")
    played_as_home_matches: List[MatchModel] = Field(alias="entity_home_team_matches")
    played_as_away_matches: List[MatchModel] = Field(alias="entity_away_team_matches")


    class Config:
        orm_mode = True



class CompAreaModel(BaseModel):

    id: int
    comp_name: constr(max_length=100)
    area_id: int
    area_name: constr(max_length=100)
    area_country_code: constr(max_length=30)
    last_update: datetime.datetime


    class Config:
        orm_mode = True



class CompCurrentSeasonModel(BaseModel):

    comp_id: int
    comp_name: constr(max_length=100)
    id: int
    season_start_date: datetime.datetime
    season_end_date: datetime.datetime
    last_update: datetime.datetime



    class Config:
        orm_mode = True



class CompModel(BaseModel):


    id: int
    comp_name: constr(max_length=100)
    comp_code: constr(max_length=30)

    plan: constr(max_length=100)
    last_update: datetime.datetime


    area: CompAreaModel = Field(alias="entity_area")
    season: CompCurrentSeasonModel = Field(alias="entity_current_season")
    teams: List[TeamModel] = Field(alias="entity_teams")


    class Config:
        orm_mode = True


