from abc import ABC, abstractmethod
from app.DAO_class.DAO_FineDataModel import FDMCompModel


class AbstractCompModelFilter(ABC):
    """classe abstraite définissant un filtre a appliquer a un comp_model
        le filtre est suivi d'une fonction validator() qui vérifie le parsing effectuée par le filtre
        l'étape de parsing et de validation avec le retour du comp_model est assurée par la fonction
        qui ne sera par override get_filtered_and_validated()

        pour l'overriding de la methode abstraite filter():
        -si une fonction 'team_match_parser()' est définie:
            on définit un dictionnaire de team_model a renvoyer que l'on renvoit avec le snippet suivant afin de pallier
            les problemes de classe de l'objet team_model, car ainsi le 'ret_team_model' renvoyé sera de la meme classe que le 'team_model'
            passé en attribut de la fonction 'team_match_parser()':

            ------------------------------------------------------------
            ret_team_model = team_model.__class__(**ret_team_model_dict)
            return ret_team_model
            ------------------------------------------------------------
        -de la meme façon l'attribution du nouveau comp_model de la fonction filter sera effectué grace au snippet suivant pour éviter les problemes
            liés a la classe du comp_model:

            ------------------------------------------------------------
            ret_comp_model = self.comp_model.__class__(**ret_comp_model_dict)
            self.comp_model = ret_comp_model
            ------------------------------------------------------------
    """


    def __init__(self, comp_model):
        self.comp_model = comp_model
        super().__init__()

    @abstractmethod
    def filter(self):
        pass


    @abstractmethod
    def validator(self):
        pass



    def get_filtered_and_validated(self):
        self.filter()
        self.validator()
        return self.comp_model



