# -*- encoding: utf-8 -*-
"""
    desarrollador: juan garcía
"""

from controller.gestor_controller import Gestor
from app import app

if __name__ == '__main__':
    g = Gestor()
    g.crear_base_de_datos() # Creamos base de datos si no existe
    g.crearTablas() # Creamos tablas de la base de datos si no existen
    g.crearPrivilegios() # Creamos los privilegios en base de datos
    app.run(debug=False, port=5001, host="0.0.0.0")