from typing import Callable, Any, List
from pydantic import BaseModel
from functools import partial


class ParseCompModelMainDecorator(object):
    """Le décorateur censé parser les données s'il est appelé dans une methode:
        l'attribut 'self._comp_model_field' doit correspondre a l'attribut d'instance 'comp_model__' de la classe dans laquelle le décorateur est appelé
        l'attribut 'self._parsed_comp_model_field' doit correspondre a l'attribut d'instance parsed_comp_model__ de la classe dans laquelle le décorateur est appelé

        the __call__ method call the functions 'check_field_error_raiser' and 'get_function_to_classmethod'
        to prepare the function to be useful
        the method 'apply_filters' is an abstract method that call the filters we want to parse
        this method must be overriden in by subclasses"""
    _filter_list: List[Callable[[Any], Any]] = []

    def __init__(self, func: Callable[[Any], Any]):
        self._func = func
        self._comp_model_field = "comp_model__"
        self._parsed_comp_model_field = "parsed_comp_model__"
        self._is_parsed_field = "is_parsed__"


    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)

    def __call__(self, instance):
        check_field_error_raiser(instance, self._comp_model_field, BaseModel.__subclasses__())
        if not check_is_parsed_error_raiser(instance, self._is_parsed_field):
            self.apply_filters(instance, getattr(instance, self._comp_model_field), self._parsed_comp_model_field)

        self._func(instance)


    def apply_filters(self, instance, comp_model, _parsed_comp_model_field):
        ret_model = comp_model.copy()
        for filters in self._filter_list:
            ret_model = filters(ret_model).filter()

        setattr(instance, _parsed_comp_model_field, ret_model)



def check_field_error_raiser(instance, _field: str, _field_type_list):
    """check if the field mentionned in _field is linked to an attribute in the class(owner)
    and if the type of the element in the _field is the wrong or not """

    if not hasattr(instance, _field):
        raise AttributeError(f"L'attribut de class '{_field}' censé définir l'objet a parser n'est pas défini")  # pragma: no cover
    else:
        if not type(getattr(instance, _field)) in _field_type_list:
            raise ValueError(f"le champ {_field} n'est pas du type demandé: l'attribut {_field} doit etre une instance "  # pragma: no cover
                             f" d'une subclasse CompModel de la classe 'BaseModel' ")


def check_is_parsed_error_raiser(instance, _is_parsed_field):
    if hasattr(instance, _is_parsed_field):
        boolean_rep = getattr(instance, _is_parsed_field)
        setattr(instance, _is_parsed_field, True)
        return boolean_rep

    else:
        raise AttributeError(f"object {instance} of class {instance.__class__} do not have attr {_is_parsed_field}, give it")  # pragma: no cover