from app.ORM_Pilot import ORM_session_management_class as script


class TestEngineManager:

    @classmethod
    def setup_method(cls):
        cls.engine_list = script.EngineManager.engine
        script.EngineManager.get_engine()

    def test_get_engine(self):
        assert len(self.engine_list) == 1
        script.EngineManager.get_engine()
        assert len(self.engine_list) == 1

    @classmethod
    def teardown_method(cls):
        cls.engine_list = []


class TestSessionManager:

    @classmethod
    def setup_method(cls):
        cls.session_list = script.SessionManager.Session_elements
        script.SessionManager.get_session()

    def test_get_session(self):
        assert len(self.session_list) == 1
        script.SessionManager.get_session()
        assert len(self.session_list) == 1

    @classmethod
    def teardown_method(cls):
        cls.session_list = []