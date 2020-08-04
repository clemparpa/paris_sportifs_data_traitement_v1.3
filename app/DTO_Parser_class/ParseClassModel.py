from app.DAO_class.DAO_FineDataModel import FDMCompModel
from pydantic import BaseModel


class ParseBaseModel:
    """classe définissant des champs requis: le champ:
        Le Champ '__comp_model__' doit contenir la data a parser de type CompNonNulModel:
        Le Champ '__parsed_comp_model' récuperera la data parsée par le décorateur s'il est appelé
        Le Champ '__is_parsed__' vérifiera si le champ __parsed_comp_model__ est déja rempli et donc s'il est
        nécessaire de parser la donnée ou non
        tous ces champ seront hérités a la classe qui doit être parsée"""

    __comp_model__: BaseModel.__subclasses__()
    __parsed_comp_model__: BaseModel.__subclasses__()
    __is_parsed__: bool = False

