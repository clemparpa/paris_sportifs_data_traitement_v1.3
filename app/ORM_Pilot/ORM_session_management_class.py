from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLAlchemy_parameters import conn_to_SQL as conn


class EngineManager:
    """classe singleton ayant pour rôle de créer ou de récupérer un engine si celui ci à déjà été crée"""
    engine = []

    @classmethod
    def get_engine(cls):
        if not cls.engine:
            engine_element = create_engine(conn.LocalDb.url, echo=False)
            cls.engine.append(engine_element)
        return cls.engine[0]





class SessionManager:
    """classe singleton ayant pour rôle de créer ou de récupérer une session si celle ci à déjà été crée"""
    Session_elements = []


    @classmethod
    def get_session(cls):
        if not cls.Session_elements:
            engine = EngineManager.get_engine()
            session_class = sessionmaker(bind=engine)
            session_element = session_class()
            cls.Session_elements.append(session_element)
        return cls.Session_elements[0]