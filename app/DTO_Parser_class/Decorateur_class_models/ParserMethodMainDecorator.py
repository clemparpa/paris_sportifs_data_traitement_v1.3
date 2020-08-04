from typing import Callable, Any, List
from pydantic import BaseModel



class ParseCompModelMainDecorator(object):
    """Le décorateur censé parser les données s'il est appelé dans une methode:
        l'attribut 'self._comp_model_field' doit correspondre a l'attribut de __comp_model__ de la metaclasse MetaParseMatch
        l'attribut 'self._parsed_comp_model_field' doit correspondre a l'attribut de __parsed_comp_model__ de la metaclasse MetaParseMatch

        the __set_name__ method call the functions 'check_field_error_raiser' and 'get_function_to_classmethod'
        to prepare the function to be useful
        the method 'apply_filters' is an abstract method that call the filters we want to parse
        this method must be overriden in by subclasses"""
    _filter_list: List[Callable[[Any], Any]] = []

    def __init__(self, func: Callable[[Any], Any]):
        self._func = func
        self._comp_model_field = "__comp_model__"
        self._parsed_comp_model_field = "__parsed_comp_model__"
        self._is_parsed_field = "__is_parsed__"


    def __call__(self, comp_id):
        self.comp_id = comp_id




    def __set_name__(self, owner, name):
        check_field_error_raiser(owner, self._comp_model_field, BaseModel.__subclasses__())
        if not check_is_parsed_error_raiser(owner, self._is_parsed_field):
            self.apply_filters(owner, getattr(owner, self._comp_model_field), self._parsed_comp_model_field)


        setattr(owner, name, get_function_to_classmethod(self._func))


    def apply_filters(self, owner, comp_model, _parsed_comp_model_field):
        ret_model = comp_model.copy()
        for filters in self._filter_list:
            ret_model = filters(ret_model).get_filtered_and_validated()

        setattr(owner, _parsed_comp_model_field, ret_model)



def get_function_to_classmethod(function: Callable[[Any], Any]) -> classmethod:
    """transform the function passed to a classmethod if it isn't """
    if isinstance(function, classmethod):
        f_cls = function
    else:
        f_cls = classmethod(function)

    return f_cls



def check_field_error_raiser(owner, _field: str, _field_type_list):
    """check if the field mentionned in _field is linked to an attribute in the class(owner)
    and if the type of the element in the _field is the wrong or not """

    if not hasattr(owner, _field):
        raise AttributeError(f"L'attribut de class '{_field}' censé définir l'objet a parser n'est pas défini")
    else:
        if not type(getattr(owner, _field)) in _field_type_list:
            raise ValueError(f"le champ {_field} n'est pas du type demandé: l'attribut {_field} doit etre une instance "
                             f" d'une subclasse CompModel de la classe 'BaseModel' ")



def check_is_parsed_error_raiser(owner, _is_parsed_field):
    if hasattr(owner, _is_parsed_field):
        boolean_rep = getattr(owner, _is_parsed_field)
        setattr(owner, _is_parsed_field, True)
        return boolean_rep


    else:
        raise AttributeError(f"class {owner} do not have attr {_is_parsed_field}, give it")