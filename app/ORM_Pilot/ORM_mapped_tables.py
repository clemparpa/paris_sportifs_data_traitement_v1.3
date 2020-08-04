from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import relationship
from SQLAlchemy_parameters import conn_to_SQL as conn
from lib import date_convert


class TableInfoMatch(conn.LocalDb.Base):
    """nom de la table : 'info_match'

    -relation One to One avec la table 'score_match' de la classe TableScoreMatch: la classe TableInfoMatch est parent
        |relation bidirectionnelle avec la table 'score_match' accessible depuis l'attribut 'entity_score_match'

    -relation One to Many avec la table 'teams' de la classe TableTeam: les classes TableTeam sont parents
        |relation bidirectionnelle avec la table 'teams' accessible depuis les attributs 'entity_home_team'
        | et 'entity_away_team', qui donnent respectivement accès aux infos de l'équipe à domicile et à l'exterieur
    """

    __tablename__ = 'info_match'


    id = Column(Integer, primary_key=True)
    match_status = Column(String(30))
    season_id = Column(Integer)
    season_year = Column(Integer)
    match_day = Column(Integer)
    comp_id = Column(Integer, ForeignKey("competitions_info.id"))
    utc_date = Column(DateTime)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    last_update = Column(DateTime)


    """attribut de la relation avec la table score_match de la class TableScoreMatch"""
    entity_score_match = relationship("TableScoreMatch", back_populates="entity_info_match", uselist=False,
                                      cascade="all, delete-orphan")

    """attributs de la relation avec la table team, pour la home_team et la away_team"""
    entity_home_team = relationship("TableTeam", foreign_keys=[home_team_id],
                                    back_populates="entity_home_team_matches", cascade="all")
    entity_away_team = relationship("TableTeam", foreign_keys=[away_team_id],
                                    back_populates="entity_away_team_matches", cascade="all")

    entity_competition = relationship("TableInfoCompetition", back_populates="entity_matchs_info", cascade="all")


    """constructeur des objets de la table info_match"""

    def __init__(self, **data_match_info):  # pragma: no cover
        self.id = data_match_info["match_id"]
        self.comp_id = data_match_info["comp_id"]
        self.match_status = data_match_info["match_status"]
        self.season_id = data_match_info["season_id"]
        self.match_day = data_match_info["match_day"]
        self.season_year = data_match_info["season_year"]
        self.FDO_home_team_id = data_match_info["FDO_home_team_id"]
        self.FDO_away_team_id = data_match_info["FDO_away_team_id"]
        self.utc_date = date_convert.convert_date(data_match_info["utc_date"])
        self.last_update = date_convert.convert_date(data_match_info["last_update"])



class TableScoreMatch(conn.LocalDb.Base):
    """nom de la table : 'score_match'

    -relation One to One avec la table 'info_match' de la classe TableInfoMatch: la classe TableInfoMatch est parent
        |relation bidirectionnelle avec la table 'info_match' accessible depuis l'attribut 'entity_info_match'
    """

    __tablename__ = 'score_match'

    id = Column(Integer, ForeignKey("info_match.id"), primary_key=True)
    winner = Column(String(30))
    duration = Column(String(30))
    half_time_home_score = Column(Integer)
    full_time_home_score = Column(Integer)
    full_time_away_score = Column(Integer)
    half_time_away_score = Column(Integer)
    last_update = Column(DateTime)

    """attribut de la relation avec la table info_match de la class TableInfoMatch"""
    entity_info_match = relationship("TableInfoMatch", back_populates="entity_score_match",
                                     cascade="all, delete-orphan", single_parent=True)

    """constructeur des objets de la table score_match"""

    def __init__(self, **data_match_score):  # pragma: no cover
        self.id = data_match_score["match_id"]
        self.winner = data_match_score["winner"]
        self.duration = data_match_score["duration"]
        self.half_time_home_score = data_match_score["half_time_home_score"]
        self.full_time_home_score = data_match_score["full_time_home_score"]
        self.full_time_away_score = data_match_score["full_time_away_score"]
        self.half_time_away_score = data_match_score["half_time_away_score"]
        self.last_update = date_convert.convert_date(data_match_score["last_update"])


class TableStandings(conn.LocalDb.Base):
    """nom de la table 'standings'

    - relation One to One avec la table 'teams' de la classe TableTeam: la classe parent est la classe TableTeam
        |relation bidirectionnelle. la table 'teams' est accessible depuis l'attribut 'entity_team'

    - relation Many to One avec la table 'competitions_info de la classe TableInfoCompetitions qui est la classe parent:
        |relation unidirectionelle qui n'est pas accessible dans cette classe

    - les colonnes comp_id, season_id, Fdo_team_id forment une clé unique
    """
    __tablename__ = 'standings'

    id = Column(Integer, ForeignKey("teams.id"), primary_key=True)

    comp_id = Column(Integer)
    season_year = Column(Integer)
    FDO_team_id = Column(Integer)

    """contrainte clé unique imposée aux 3 colonnes comp_id, season_year et team_id"""
    __table_args__ = (UniqueConstraint(comp_id, season_year, FDO_team_id),)

    position = Column(Integer)
    team_name = Column(String(50))
    nb_de_matchs = Column(Integer)
    nb_de_win = Column(Integer)
    nb_de_nul = Column(Integer)
    nb_de_lose = Column(Integer)
    points = Column(Integer)
    buts_marques = Column(Integer)
    buts_encaisses = Column(Integer)


    entity_team = relationship("TableTeam", back_populates="entity_standing", cascade="all, delete-orphan",
                               single_parent=True)

    def __init__(self, **data_standings):  # pragma: no cover
        self.comp_id = data_standings["comp_id"]
        self.season_year = data_standings["season_year"]
        self.FDO_team_id = data_standings["FDO_team_id"]
        self.position = data_standings["position"]
        self.team_name = data_standings["team_name"]
        self.nb_de_matchs = data_standings["nb_de_matchs"]
        self.nb_de_win = data_standings["nb_de_win"]
        self.nb_de_nul = data_standings["nb_de_nul"]
        self.nb_de_lose = data_standings["nb_de_lose"]
        self.points = data_standings["points"]
        self.buts_marques = data_standings["buts_marques"]
        self.buts_encaisses = data_standings["buts_encaisses"]


class TableTeam(conn.LocalDb.Base):
    """nom de la table : 'teams'

    -relation Many To One avec la table 'competitions_info' de la table 'TableInfoCompetition' qui est la table parent:
        |relation unidirectionnelle qui n'est pas accessible depuis cette classe

    -relation One To One avec la table 'standings' de la classe 'TableStandings' la classe TableTeam est parent:
        |relation bidirectionnelle qui est accessible dans cette classe par l'attribut 'entity_standings'

    -relation Many to One avec la table 'info_match' de la classe TableInfoMatch. les classes Team sont parents:
        |relation bidirectionnelle accessible grace aux attributs entity_home_team_matches, entity_away_team_matches,
        |respectivement les infos des matchs dans lesquelles l'équipe a été a domicile, et à l'exterieur

    -les colonnes comp_id, season_year, team_id forment une clé unique"""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)

    comp_id = Column(Integer, ForeignKey("competitions_info.id"))
    season_year = Column(Integer)
    FDO_team_id = Column(Integer)


    __table_args__ = (UniqueConstraint("comp_id", "season_year", "FDO_team_id", name="partition_team_unique"),)

    team_name = Column(String(100))
    team_area = Column(String(100))
    team_short_name = Column(String(30))
    team_tla = Column(String(30))
    founded = Column(Integer)
    venue = Column(String(200))
    club_colors = Column(String(100))
    last_update = Column(DateTime)

    # lien de relation avec la table FDOTeamsTable
    entity_home_team_matches = relationship("TableInfoMatch", back_populates="entity_home_team",
                                            cascade="all, delete-orphan",
                                            foreign_keys=[TableInfoMatch.home_team_id])

    entity_away_team_matches = relationship("TableInfoMatch", back_populates="entity_away_team",
                                            cascade="all, delete-orphan",
                                            foreign_keys=[TableInfoMatch.away_team_id])

    entity_standing = relationship("TableStandings", back_populates="entity_team", uselist=False,
                                   cascade="all, delete-orphan", foreign_keys=[TableStandings.id,
                                                                               TableStandings.comp_id,
                                                                               TableStandings.season_year,
                                                                               TableStandings.FDO_team_id])

    entity_competition = relationship("TableInfoCompetition", back_populates="entity_teams", cascade="all")

    """constructeur de la table teams"""
    def __init__(self, **data_teams):  # pragma: no cover
        self.comp_id = data_teams["comp_id"]
        self.season_year = data_teams["season_year"]
        self.FDO_team_id = data_teams["FDO_team_id"]
        self.team_name = data_teams["team_name"]
        self.team_area = data_teams["team_area"]
        self.team_short_name = data_teams["team_short_name"]
        self.team_tla = data_teams["team_tla"]
        self.founded = data_teams["founded"]
        self.venue = data_teams["venue"]
        self.club_colors = data_teams["club_colors"]
        self.last_update = date_convert.convert_date(data_teams["last_update"])

#--------------------------------------------------------------------------------------------------------------
# Tables liées aux competitions (competitions_info, competitions_current_season, competitions_area)
#--------------------------------------------------------------------------------------------------------------


class TableInfoCompetition(conn.LocalDb.Base):
    """ le nom de la table est 'competitions_info'

    -relation One to One avec la table 'competitions_area' de la classe TableAreaCompetition. TableInfoCompetition est
    la classe parent:
        |relation unidirectionnelle accessible depuis cette classe par l'attribut 'entity_area'

    -relation One to One avec la table 'competitions_current_season' de la classe TableCurrentSeasonCompetition.
    TableInfoCompetition est la classe parent:
        |relation unidirectionnelle accessible depuis cette classe par l'attribut 'entity_current_season'

    -relation One to Many avec la table 'teams' de la class TableTeam. TableInfoCompetition est la classe parent:
        |relation unidirectionnelle accessible depuis cette classe par l'attribut 'entity_teams'

    -relation One to Many avec la table 'standings' de la class TableStandings. TableInfoCompetition est
    la classe parent:
        |relation unidirectionnelle accessible depuis cette classe par l'attribut 'entity_standings'
    """
    __tablename__ = 'competitions_info'

    id = Column(Integer, primary_key=True)
    comp_name = Column(String(100))
    comp_code = Column(String(30))

    plan = Column(String(100))
    last_update = Column(DateTime)


    entity_area = relationship("TableAreaCompetition", uselist=False, cascade="all, delete-orphan")
    entity_current_season = relationship("TableCurrentSeasonCompetition", uselist=False, cascade="all, delete-orphan")

    entity_teams = relationship("TableTeam", back_populates="entity_competition", cascade="all, delete-orphan")

    entity_matchs_info = relationship("TableInfoMatch", back_populates="entity_competition",
                                      cascade="all, delete-orphan")


    def __init__(self, **data_comp_info):  # pragma: no cover
        self.id = data_comp_info["comp_id"]
        self.comp_name = data_comp_info["comp_name"]
        self.comp_code = data_comp_info["comp_code"]
        self.plan = data_comp_info["plan"]
        self.last_update = date_convert.convert_date(data_comp_info["last_update"])




class TableAreaCompetition(conn.LocalDb.Base):
    """nom de la table : 'competitions_area'

    accessible depuis la table competitions_info

    """
    __tablename__ = 'competitions_area'


    id = Column(Integer, ForeignKey('competitions_info.id'), primary_key=True)
    comp_name = Column(String(100))
    area_id = Column(Integer)
    area_name = Column(String(100))
    area_country_code = Column(String(30))
    last_update = Column(DateTime)


    def __init__(self, **data_comp_area):  # pragma: no cover
        self.id = data_comp_area["comp_id"]
        self.comp_name = data_comp_area["comp_name"]
        self.area_id = data_comp_area["area_id"]
        self.area_name = data_comp_area["area_name"]
        self.area_country_code = data_comp_area["area_country_code"]
        self.last_update = date_convert.convert_date(data_comp_area["last_update"])




class TableCurrentSeasonCompetition(conn.LocalDb.Base):
    """nom de la table 'competitions_current_season'

    accessible depuis la table competitions_info

    """
    __tablename__ = 'competitions_current_season'

    comp_id = Column(Integer, ForeignKey('competitions_info.id'))
    comp_name = Column(String(100))
    id = Column(Integer, primary_key=True)
    season_start_date = Column(DateTime)
    season_end_date = Column(DateTime)
    last_update = Column(DateTime)



    def __init__(self, **data_comp_season):  # pragma: no cover
        self.comp_id = data_comp_season["comp_id"]
        self.comp_name = data_comp_season["comp_name"]
        self.id = data_comp_season["season_id"]
        self.season_start_date = date_convert.convert_date_only_day(data_comp_season["season_start_date"])
        self.season_end_date = date_convert.convert_date_only_day(data_comp_season["season_end_date"])
        self.last_update = date_convert.convert_date(data_comp_season["last_update"])


class TableRequestErrorLog(conn.LocalDb.Base):
    """nom de la table 'request_log_error'

    cette table contient les logs d'erreur des requêtes effectuées a l'api football_data_org.
    elle n'est liée a aucune autre table de ce mapping
    """

    __tablename__ = 'request_log_error'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200))
    status_code = Column(Integer)
    date = Column(DateTime)
    msg = Column(String(100))


    def __init__(self, **data_log_list):  # pragma: no cover
        self.url = data_log_list["_RequestLog__url"]
        self.status_code = data_log_list["_RequestLog__status_code"]
        self.date = data_log_list["_RequestLog__date"]
        self.msg = data_log_list["_RequestLog__msg"]


