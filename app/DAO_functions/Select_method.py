from app.ORM_Pilot import DTIC_mapped_class as models
from app.ORM_Pilot import ORM_session_management_class as mana
from app.ORM_Pilot import ORM_mapped_tables as tables


class Select:  # pragma: no cover
    """classe permettant de Selectionner dans les tables sql les objets competitions
        comme des objets de la class DTIC_mapped_class"""

    __session = mana.SessionManager.get_session()

    def __init__(self, comp_id):
        __orm_competition_object = self.__session.query(tables.TableInfoCompetition).get(comp_id)
        self.competition_model = models.CompModel.from_orm(__orm_competition_object)





