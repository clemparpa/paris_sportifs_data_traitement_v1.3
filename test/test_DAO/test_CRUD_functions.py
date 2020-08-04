from app.DAO_functions import CRUD_functions as Crud
from app.ORM_Pilot import DTIC_mapped_class as model




class TestSelect:

    def test_select_comp(self):
        assert type(Crud.select_comp(2021)) == model.CompModel


    def test_select_all_comp(self):
        assert type(Crud.select_all_comp()) == list