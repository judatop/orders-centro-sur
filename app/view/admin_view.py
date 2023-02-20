from flask.ctx import copy_current_request_context
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms.admin_form import AdministracionForm
from controller import administracion_controller
from flask import flash, redirect, render_template, url_for
from app import app
import threading

from controller.gestor_controller import Gestor
from controller import usuarios_controller


@app.route('/administracion.html', methods=['GET', 'POST'])
@login_required
def administracion():
    privilegio = usuarios_controller.verificar_privilegios("Catastros")
    if privilegio:
        g = Gestor()
        params = []
        adminForm = AdministracionForm()
        params.append(adminForm)  # params[0]

        if adminForm.validate_on_submit():  # Cargar catastros

            archivoCliente = adminForm.archivoCliente.data
            archivoHistorialConsumos = adminForm.archivoHistorialConsumos.data
            archivoOrden = adminForm.archivoOrden.data
            archivoMarcasMedidores = adminForm.archivoMarcasMedidores.data

            if archivoCliente:
                # Cargamos catastro de clientes
                rutaCatastroClientes = g.rutaCatastros + secure_filename(archivoCliente.filename)
                archivoCliente.save(rutaCatastroClientes)
                
                @copy_current_request_context
                def enviar_archivo_cliente(rutaCatastroClientes):
                    administracion_controller.cargarCatastroClientes(rutaCatastroClientes)

                print("INICIO DE HILO")
                thread = threading.Thread(name='cargo_catastro_cliente', target=enviar_archivo_cliente, args=[rutaCatastroClientes])
                thread.start()

            if archivoHistorialConsumos:
                # Cargamos catastro de historial de consumos
                rutaCatastroHistorial = g.rutaCatastros + secure_filename(archivoHistorialConsumos.filename)
                archivoHistorialConsumos.save(rutaCatastroHistorial)

                @copy_current_request_context
                def enviar_archivo_historial(rutaCatastroHistorial):
                    administracion_controller.cargarCatastroHistorialConsumos(rutaCatastroHistorial)

                print("INICIO DE HILO")
                thread = threading.Thread(name='cargo_catastro_historial', target=enviar_archivo_historial, args=[rutaCatastroHistorial])
                thread.start()

            if archivoOrden:
                # Cargamos catastro de ordenes
                rutaCatastroOrdenes = g.rutaCatastros + secure_filename(archivoOrden.filename)
                archivoOrden.save(rutaCatastroOrdenes)

                @copy_current_request_context
                def enviar_archivo_orden(rutaCatastroOrdenes):
                    administracion_controller.cargarCatastroOrdenes(rutaCatastroOrdenes)

                print("INICIO DE HILO")
                thread = threading.Thread(name='cargo_catastro_ordenes', target=enviar_archivo_orden, args=[rutaCatastroOrdenes])
                thread.start()

            if archivoMarcasMedidores:
                # Cargamos catastro de Ing. Edgar de marcas de medidores
                administracion_controller.cargarCatastroMarcasMedidores(archivoMarcasMedidores)

        return render_template('administracion.html', segment='administracion', params=params)
    return redirect(url_for('index'))

"""     except Exception as ex:
        flash('Ha ocurrido un error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message) """

