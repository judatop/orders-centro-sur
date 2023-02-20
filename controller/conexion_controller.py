from peewee import *


class Conexion:
    db = MySQLDatabase('orden', user='root', password='gatojuda', host='localhost', port=3306, autoconnect=False)
