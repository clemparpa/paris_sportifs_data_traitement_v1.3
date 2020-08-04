from functools import wraps
from app.DAO_class.DAO_Match_Non_Nuls import CompNonNulModel, MatchNonNulModel, TeamNonNulModel
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, Type, Union, overload
from app.DAO_functions import CRUD_functions as Crud
from ast import literal_eval
import sys



class ParseMatch(type):

    def __new__(mcs, name, bases, dict):

        classe = super().__new__(mcs, name, bases, dict)
        classe.__comp_model__ = None
        classe.__parsed_comp_model__ = None
        classe.__is_parsed__ = False
        return classe




def classe_parser(cls):

    for name, method in cls.__dict__.items():
        if hasattr(method, "__to_parse__"):
            print("parsed")
            #setattr(method, "comp_model", cls.__parsed_comp_model__)

        else:
            print("not parsed")
            #setattr(method, "comp_model", cls.__comp_model__)

    return cls


def parser(func):
    f_cls = _prepare_function(func)
    f_cls.__to_parse__ = True
    return f_cls


def _finished_match_parser(comp_model: CompNonNulModel):

    def team_match_parser(team_model: TeamNonNulModel):

        def match_filter(match_model: MatchNonNulModel):
            if match_model.match_status == 'FINISHED':
                return match_model

        ret_team_model_dict = {
            "season_year": team_model.season_year,
            "standing": team_model.standing,
            "id": team_model.id,
            "played_as_home_matches": list(filter(match_filter, team_model.played_as_home_matches)),
            "played_as_away_matches": list(filter(match_filter, team_model.played_as_away_matches)),
        }

        ret_team_model = TeamNonNulModel(**ret_team_model_dict)
        return ret_team_model

    ret_comp_model_dict = {
        "id": comp_model.id,
        "teams": list(map(team_match_parser, comp_model.teams)),
    }

    ret_comp_model = CompNonNulModel(**ret_comp_model_dict)
    return ret_comp_model



def _finished_match_validator(comp_model: CompNonNulModel):

    match_list = []
    for team in comp_model.teams:
        matchs = team.played_as_home_matches + team.played_as_away_matches
        match_list.extend(matchs)

    error_list = []
    for match in match_list:
        if match.match_status != 'FINISHED':
            error_list.append(match)

    if len(error_list) > 0:
        return_error = ""
        for match in error_list:
            str_error = f"le match {match.id}, opposant les équipes {match.home_team_id}, {match.away_team_id}, a le statut {match.match_status} \n"
            return_error += str_error

        raise ValueError(return_error)

    else:
        return comp_model


def _prepare_function(function: Callable) -> classmethod:
    if isinstance(function, classmethod):
        f_cls = function
    else:
        f_cls = classmethod(function)

    return f_cls


def _field_error_raiser(owner, _field: str):
    if not hasattr(owner, _field):
        raise AttributeError("L'attribut de class '__comp_model__' censé définir l'objet a parser n'est pas défini")
    else:
        if not type(getattr(owner, _field)) == CompNonNulModel:
            raise ValueError(f"le champ {_field} n'est pas du type demandé: l'attribut {_field} doit etre une instance"
                             f"de la class CompNonNulModel")



def _model_parse(owner, _parse_field, _comp_field):

    if hasattr(owner, _parse_field):
        if getattr(owner, _parse_field):
            return _finished_match_validator(getattr(owner, _comp_field))

        else:
            return _finished_match_validator(_finished_match_parser(getattr(owner, _comp_field)))

    else:
        setattr(owner, _parse_field, True)
        _model_parse(owner, _parse_field, _comp_field)



class CompModelParser(object):

    def __init__(self, func: Callable):
        self._func = func


    def __set_name__(self, owner, name):
        _field_error_raiser(owner, "__comp_model__")
        self._save_atrr = getattr(owner, "__comp_model__")
        self._owner = owner
        parsed_comp_model = _finished_match_parser(getattr(owner, "__comp_model__"))
        validated_comp_model = _finished_match_validator(parsed_comp_model)
        setattr(owner, "__parsed_comp_model__", validated_comp_model)
        prepared_func = _prepare_function(self._func)
        setattr(owner, name, prepared_func)




@classe_parser
class Test_wola(metaclass=ParseMatch):


    __comp_model__ = "__comp_model__"#CompNonNulModel.parse_obj(Crud.select_comp(2021))
    __parsed_comp_model__ = "__parsed_comp_model__"

    """
    @CompModelParser
    def testeur_func(self):

        lis = []
        testeur = 0
        for els in self.__comp_model__.teams:
            match_list = els.played_as_home_matches + els.played_as_home_matches
            lis.extend(match_list)

        for els in lis:
            if els.match_status != 'FINISHED':
                print(els.match_status)


    @classmethod
    def hello(cls):
        for i in range(10):
            print("\n")
        lis = []
        testeur = 0
        for els in cls.__comp_model__.teams:
            match_list = els.played_as_home_matches + els.played_as_home_matches
            lis.extend(match_list)

        for els in lis:
            if els.match_status != 'FINISHED':
                print(els.match_status)
    """

    @parser
    def halo(self):
        return 1

    @classmethod
    def halo2(self):
        return 1



print(Test_wola.halo())




"""
def team_match_parser(team_model: TeamNonNulModel):

    def match_filter(match_model: MatchNonNulModel):
        if match_model.match_status == 'FINISHED':
            return match_model


    ret_model_dict = {
        "season_year": team_model.season_year,
        "standing": team_model.standing,
        "id": team_model.id,
        "played_as_home_matches": list(filter(match_filter, team_model.played_as_home_matches)),
        "played_as_away_matches": list(filter(match_filter, team_model.played_as_away_matches)),
        }

    ret_team_model = TeamNonNulModel(**ret_model_dict)

    return ret_team_model



a = Crud.select_comp(2021).teams
lis = []
for team in a:
    team = team_match_parser(team)
    for match in team.played_as_home_matches:
        print(match.match_status)
    for match in team.played_as_away_matches:
        print(match.match_status)

    for match in team.played_as_home_matches:
        if match.match_status == 'FINISHED':
            lis.append(match)
            pass
    for match in team.played_as_away_matches:
        if match.match_status == 'FINISHED':
            lis.append(match)

for els in lis:
    print(els.match_status)
"""


