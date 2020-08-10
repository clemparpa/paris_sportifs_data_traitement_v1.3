from app.DTO_Parser_class.Filter_class.Finished_Match_Filter_class import FinishedMatchCompModelFilter
from app.DTO_Parser_class.Filter_class.Implement_Serie_Nul_Match_Filter_class import ImplementSerieNulCompModelFilter
from app.DTO_Parser_class.Filter_class.Implement_Team_Info_Filter_Class import ImplementTeamInfoCompModelFilter
from app.DTO_Parser_class.Filter_class.Implement_index_nul_Filter_class import ImplementIndexNulCompModelFilter
from app.DTO_Parser_class.Filter_class.Implement_In_Home_Team_Index_Filter_Class import ImplementInHomeTeamIndexCompModelFilter
from app.DTO_Parser_class.Filter_class.Implement_CompNonNul_matches_Filter_Class import ImplementMatchesCompModelFilter
from app.DTO_Parser_class.Decorateur_class_models.ParserMainDecorator import ParseCompModelMainDecorator


class MatchNonNulDecorator(ParseCompModelMainDecorator):
    """décorateur pour une methode d'une classe héritée de la class ParseBaseModel du script ParseClassModel
        le décorateur est hérité de la classe ParseCompModelMainDecorator
        pour appliquer des filtres sur la data accessible par l'attribut "__parsed_comp_model__" de la classe décorée
        on ajoute les filtres dans l'ordre d'éxecution de ceci dans l'attribut _filter_list
        veiller a ce que les filtres renvoie bien un comp_model dans leur méthode get_filtered_validated()
        Ce décorateur enleve les matchs non terminés du comp_model et envoie un nouvel objet comp_model parsé
        a l'attribut "__parsed_comp_model__" """

    _filter_list = [FinishedMatchCompModelFilter, ImplementIndexNulCompModelFilter, ImplementInHomeTeamIndexCompModelFilter,
                    ImplementTeamInfoCompModelFilter, ImplementSerieNulCompModelFilter, ImplementMatchesCompModelFilter]