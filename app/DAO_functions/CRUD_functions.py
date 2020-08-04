from app.DAO_functions import Select_method
from app.CompetitionMetadata import FDO_competitions as comp_list



def select_comp(comp_id: int):

    return Select_method.Select(comp_id=comp_id).competition_model



def select_all_comp():

    comp_object_list = []
    for comp_ids in comp_list.FdoCompetitions.leagues_list:
        comp_obj = select_comp(comp_id=comp_ids)
        comp_object_list.append(comp_obj)

    return comp_object_list
