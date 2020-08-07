from sqlalchemy.ext.declarative import declarative_base



"""classe contenant comme attributs les informations de connexion à la base local"""


class LocalDb:
    type = 'mysql'
    lib = 'pymysql'
    host = 'localhost'
    port = '3306'
    user = 'root'
    password = 'admin'
    name = 'paris_sportifsv1.3'

    #url servant a la connexion à la base
    url = f"{type}+{lib}://{user}:{password}@{host}:{port}/{name}"

    Base = declarative_base()

