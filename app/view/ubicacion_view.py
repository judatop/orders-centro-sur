from flask import render_template, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect

from app import app
from controller import orden_controller, instalacion_controller, medidor_controller
import folium


@app.route('/ubicacionorden/<int:numero_orden>', methods=['GET', 'POST'])
@login_required
def ubicacionorden(numero_orden):
    try:
        orden = orden_controller.obtener_orden(numero_orden)
        instalacion = instalacion_controller.obtener_instalacion(
            orden.instalacion_id)
        medidor = medidor_controller.obtener_medidor_por_instalacion(
            instalacion.numero)

        coordenadaX = instalacion.coordenadaX
        coordenadaY = instalacion.coordenadaY
        
        start_coords = (coordenadaX, coordenadaY)
        folium_map = folium.Map(location=start_coords, zoom_start=14, title="Instalación de la orden "+str(numero_orden))
        tooltip = "Click me!"

        folium.Marker([coordenadaX, coordenadaY], popup="Instalación "+str(instalacion.numero)+" del medidor "+str(medidor.numero), tooltip=tooltip).add_to(folium_map)

        return folium_map._repr_html_()


    except TemplateNotFound:
        return render_template('page-404.html'), 404
