from app.DTO_Parser_class.Decorateur_class_models.ParserMethodMainDecorator import ParseCompModelMainDecorator
from app.DTO_Parser_class.Filters_class.finished_match_filter_class import FinishedMatchFilter
from app.DTO_Parser_class.Filters_class.index_nul_match_filter_class import ImplementIndexNulMatchFilter
from app.DTO_Parser_class.Filters_class.serie_nul_match_filter_class import ImplementSerieNulMatchFilter
from app.DTO_Parser_class.Filters_class.index_in_home_team_index_filter_class import ImplementHomeTeamIndexFilter
from app.DTO_Parser_class.Filters_class.unique_comp_matches_filter_class import ImplementCompModelMatches


class MatchNonNulDecorator(ParseCompModelMainDecorator):
    """décorateur pour une methode d'une classe héritée de la class ParseBaseModel du script ParseClassModel
        le décorateur est hérité de la classe ParseCompModelMainDecorator
        pour appliquer des filtres sur la data accessible par l'attribut "__parsed_comp_model__" de la classe décorée
        on ajoute les filtres dans l'ordre d'éxecution de ceci dans l'attribut _filter_list
        veiller a ce que les filtres renvoie bien un comp_model dans leur méthode get_filtered_validated()
        Ce décorateur enleve les matchs non terminés du comp_model et envoie un nouvel objet comp_model parsé
        a l'attribut "__parsed_comp_model__" """

    _filter_list = [FinishedMatchFilter, ImplementIndexNulMatchFilter, ImplementHomeTeamIndexFilter, ImplementSerieNulMatchFilter, ImplementCompModelMatches]