"""
data_compo_info = {"comp_id" : 2021, "comp_name": "michel", "comp_code": "mich", "plan": "TierOne",
                  "last_update": '2019-09-26T15:34:45Z'}

data_compo_area = {"comp_id": 2021, "comp_name": "michel", "area_id": 20234, "area_name": "LouBrazil", "area_country_code": "Bra",
                  "last_update": '2019-09-26T15:34:45Z'}

data_compo_season = {"comp_id": 2021, "comp_name": "michel", "season_id": 2034,
                    "season_start_date": '2019-09-26T15:34:45Z',
                    "season_end_date": '2019-09-30T15:34:45Z',
                    "last_update": '2019-09-26T15:34:45Z'}

data_match_info = {"match_status": "FINISHED", "match_id": 204392, "season_id": 2034, "match_day": 3,
                   'last_update': '2019-09-26T15:34:45Z'}

data_match_score = {'match_id': 204392, 'winner': 'HOME_TEAM', 'duration': 'REGULAR', 'half_time_home_score': 4,
                    'half_time_away_score': 0, 'full_time_home_score': 4, 'full_time_away_score': 1,
                    'last_update': '2019-09-26T15:34:45Z'}

team_dict1 = {'FDO_team_id': 64, "comp_id": 2021, "season_year": 2019, "team_name": "zbra", "team_area": "tamere",
              "team_short_name": "tm", "team_tla": "tm", "founded": 1984, "venue": "123 rue Bidon", "club_colors": "red"
              ,"last_update": '2019-09-26T15:34:45Z'}

team_dict2 = {'FDO_team_id': 65, "comp_id": 2021, "season_year": 2019, "team_name": "zbro", "team_area": "tamere2",
              "team_short_name": "tm2", "team_tla": "tm2", "founded": 1974, "venue": "124 rue Bidon", "club_colors": "green"
              ,"last_update": '2019-09-26T15:34:45Z'}

standing_dict1 = {"comp_id":2021, "position":2, "FDO_team_id":64, "team_name":"zbra",
                  "nb_de_matchs":12, "nb_de_win": 8, "nb_de_nul": 2, "nb_de_lose": 2,
                  "points": 28, "buts_marques": 15, "buts_encaisses": 6}

standing_dict2 = {"comp_id":2021, "position":1, "FDO_team_id":65, "team_name":"zbro",
                  "nb_de_matchs":15, "nb_de_win": 11, "nb_de_nul": 2, "nb_de_lose": 2,
                  "points": 45, "buts_marques": 27, "buts_encaisses": 4}


log_dict = {'_RequestLog__url': 'test.com', '_RequestLog__status_code': 302,
            '_RequestLog__date': datetime.datetime(2020, 6, 21, 14, 44, 29, 98412), '_RequestLog__msg': 'erreur inconnue'}



engine = conn_manager.EngineManager.get_engine()
conn.LocalDb.Base.metadata.create_all(engine, checkfirst=True)
session = conn_manager.SessionManager.get_session()


info_match = TableInfoMatch(**data_match_info)
score_match = TableScoreMatch(**data_match_score)
team1 = TableTeam(**team_dict1)
team2 = TableTeam(**team_dict2)
standing1 = TableStandings(**standing_dict1)
standing2 = TableStandings(**standing_dict2)
logger = TableRequestErrorLog(**log_dict)
info_comp = TableInfoCompetition(**data_compo_info)
area_comp = TableAreaCompetition(**data_compo_area)
season_comp = TableCurrentSeasonCompetition(**data_compo_season)


info_match_del = session.query(TableInfoMatch).get(info_match.id)
info_score_del = session.query(TableScoreMatch).get(score_match.id)
team1_del = session.query(TableTeam).get(team1.id)
team2_del = session.query(TableTeam).get(team2.id)
standing1_del = session.query(TableStandings).get(standing1.id)
standing2_del = session.query(TableStandings).get(standing2.id)
logger_del = session.query(TableRequestErrorLog).get(logger.id)
info_comp_del = session.query(TableInfoCompetition).get(info_comp.id)
area_comp_del = session.query(TableAreaCompetition).get(area_comp.id)
season_comp_del = session.query(TableCurrentSeasonCompetition).get(season_comp.id)


list_to_add = [info_match, score_match, team1, team2, standing1, standing2, logger, info_comp, area_comp, season_comp]
list_to_delete = [info_match_del, info_score_del, team1_del, team2_del, standing1_del, standing2_del, logger_del,
                  info_comp_del, area_comp_del, season_comp_del]

session.add(team1)
#session.add_all(list_to_add)
#for els in list_to_delete:
#    session.delete(els)

session.commit()
session.close()
"""