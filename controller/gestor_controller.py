import traceback
from controller.conexion_controller import Conexion
from model.asistenteadministrativo import AsistenteAdministrativo
from model.asistentejefe import AsistenteJefe
from model.cliente import Cliente
from model.cliente_instalacion import Cliente_Instalacion
from model.medidor import Medidor
from model.parametrizacion import Parametrizacion
from model.privilegio import Privilegio
from model.prueba import Prueba
from model.sello import Sello
from model.transformadordedistribucion import TransformadorDeDistribucion
from model.transformadordemedida import TransformadorDeMedida
from model.verificacion import Verificacion
from model.anomaliaencontrada import AnomaliaEncontrada
from model.fotografia import Fotografia
from model.historialmedidor import HistorialMedidor
from model.historialrdico2 import HistorialRDICO2
from model.instalacion import Instalacion
from model.lectura import Lectura
from model.lecturatotal import LecturaTotal
from model.perfildecarga import PerfilDeCarga
from model.rdico2 import RDICO2
from model.revisor import Revisor
from model.usoenergiaverificado import UsoEnergiaVerificado
from model.accionserviciocliente import AccionServicioCliente
from model.cambiomaterial import CambioMaterial
from model.gruporevisor import GrupoRevisor
from model.orden import Orden
from model.rdico5 import RDICO5
from model.usuario import Usuario
from model.medidortemp import MedidorTemp
from model.contactotecnico import ContactoTecnico
from model.accionanomalia import AccionAnomalia
from model.rdico2_anomalia_accion import RDICO2_Anomalia_Accion
import pymysql

class Gestor():
    rutaCatastros = "catastros/"
    rutaImagenes = "app/static/assets/img/fotografias/"
    rutaLecturas = "lecturas/"
    rutaPerfiles = "perfiles/"
    host = "localhost"
    db_user = "root"
    db_password = "gatojuda"

    def crear_base_de_datos(self):
        try:
            conn = pymysql.connect(host= self.host, user=self.db_user, password=self.db_password)
            conn.cursor().execute('CREATE DATABASE orden')
            conn.close()     
        except Exception as ex:
            print("BASE DE DATOS YA EXISTE")
            


    def crearTablas(self):
        try:
            db = Conexion.db
            db.connect()
            db.create_tables([Cliente, Instalacion, Medidor, Parametrizacion, Prueba, Sello, TransformadorDeDistribucion,
                            TransformadorDeMedida, Verificacion, Revisor, Revisor, AnomaliaEncontrada, Fotografia,
                            HistorialRDICO2, HistorialMedidor, Lectura, LecturaTotal, PerfilDeCarga, RDICO2, UsoEnergiaVerificado, AsistenteAdministrativo,
                            AccionServicioCliente, CambioMaterial, GrupoRevisor, Orden, RDICO5, Usuario, MedidorTemp,
                            Cliente_Instalacion, ContactoTecnico, AsistenteJefe, AccionAnomalia, RDICO2_Anomalia_Accion, Privilegio,
                            Privilegio.usuarios.get_through_model(),
                            RDICO2.fotografias.get_through_model(),
                            RDICO2.usosEnergiaVerificado.get_through_model(),
                            RDICO2.pruebas.get_through_model(),
                            RDICO2.sellos.get_through_model(),
                            RDICO2.transformadoresDeDistribucion.get_through_model(),
                            RDICO2.transformadoresDeMedida.get_through_model(),
                            RDICO2.historiales.get_through_model(),
                            RDICO2.lecturas.get_through_model(),
                            RDICO2.anomalias.get_through_model()])
            cursor = db.cursor()
        except Exception as ex:
            traceback.print_exc()
        finally:
            db.close()


    def crearPrivilegios(self):
        try:
            db = Conexion.db
            db.connect()
            privilegio = Privilegio.get_or_none(Privilegio.tipo == "GrupoRevisor")
            if not privilegio:
                privilegio = Privilegio(tipo="GrupoRevisor", usuario=False, asistente_admin=False, asistente_jefe=False, grupo_revisor=False, revisor=False, catastro=False, orden=True, administrar_orden=False)
                privilegio.save()
            privilegio = Privilegio.get_or_none(Privilegio.tipo == "AsistenteJefe")
            if not privilegio:
                privilegio = Privilegio(tipo="AsistenteJefe", usuario=False, asistente_admin=False, asistente_jefe=False, grupo_revisor=False, revisor=False, catastro=False, orden=False, administrar_orden=True)
                privilegio.save()
            privilegio = Privilegio.get_or_none(Privilegio.tipo == "AsistenteAdmin")
            if not privilegio:    
                privilegio = Privilegio(tipo="AsistenteAdmin", usuario=False, asistente_admin=False, asistente_jefe=False, grupo_revisor=False, revisor=False, catastro=False, orden=False, administrar_orden=True)
                privilegio.save()
        except Exception as ex:
            traceback.print_exc()
        finally:
            db.close()

        
