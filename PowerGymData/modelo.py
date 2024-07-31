import sqlite3
import re
from datetime import datetime

# ##############################################
# MODELO
# ##############################################

def decorador_aviso_abm(funcion):
    """
    Metodo decorador de funciones alta, borrar y actualizar_user
    de clase GestorUsuarios, que imprime por consola la fecha y
    hora del momento de la alta, baja o modificacion de la tabla
    usuarios.
    """
    def envoltura(*args):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        if funcion(*args) == "alta":
            print("Alta de registro:------" + fecha)
            return True
        if funcion(*args) == "borrar":
            print("Baja de registro-------" + fecha)
            return True
        if funcion(*args) == "actualizar_user":
            print("Actualiza registro--------" + fecha)

        if funcion(*args) != "alta" and funcion(*args) != "borrar" and funcion(*args) != "actualizar_user":
            print("Operación no reconocida")

    return envoltura


class ConexionDB:
    """
    Metodo encargado de establecer la conexion con la base de datos
    """
    def __init__(self):
        self.con = self.conectar()

    def conectar(self):
        try:
            return sqlite3.connect('gimnasio.db')
        except sqlite3.Error as e:
            print("Error al conectar a la base de datos:", e)


class GestorUsuarios:
    def __init__(self):
        self.db = ConexionDB()
        self.crear_tabla()

    def crear_tabla(self):
        """
        Metodo que se encarga de crear la tabla **usuarios** si no existe,
        la cual consta de 7 campos:
        dni, nombre, edad, nacionalidad, altura, peso, telefono.
        """
        cursor = self.db.con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS usuarios(
                 dni INTEGER PRIMARY KEY,
                 nombre TEXT,
                 edad INTEGER,
                 nacionalidad TEXT,
                 altura INTEGER,
                 peso INTEGER,
                 telefono INTEGER)""" 
        cursor.execute(sql)
        self.db.con.commit()

    @decorador_aviso_abm
    def alta(self, dni, nombre, edad, nacionalidad, altura, peso, telefono):
        """
        Metodo que da de alta al usuario en la base de datos.
        """
        if self.validar_nombre(nombre):
            try:
                cursor = self.db.con.cursor()
                data = (dni, nombre, edad, nacionalidad, altura, peso, telefono)
                sql = """INSERT INTO usuarios(dni, nombre, edad, nacionalidad, altura, peso, telefono)
                         VALUES(?,?,?,?,?,?,?)"""
                cursor.execute(sql, data)
                self.db.con.commit()
                print("Estoy en alta todo ok")
                return "alta"
            except Exception as e:
                print(f"Error al insertar usuario: {e}")
                return False  # retorna False en caso de error
        else:
            print("Error al validar el nombre.")
            return False  # Retorna False si la validación del nombre falla

    def validar_nombre(self, nombre):
        """
        Metodo que valida el dato recibido como parametro,
        para que cumpla con las condiciones establecidas.
        """
        patron = "^[A-Za-záéíóú]*$"
        return re.match(patron, nombre) is not None

    @decorador_aviso_abm
    def borrar(self, dni):
        """
        Metodo que borra en la base de datos el usuario seleccionado
        en la aplicacion.
        """
        try:
            cursor = self.db.con.cursor()
            sql = "DELETE FROM usuarios WHERE dni = ?"
            cursor.execute(sql, (dni,))
            self.db.con.commit()

            return "borrar"
        except Exception as e:
            print(f"Error al borrar usuario con DNI {dni}: {e}")
            return False  # Retorna False si ocurre un error

    @decorador_aviso_abm
    def actualizar_user(self, nombre, dni):
        """
        Metodo encargado de actualizar en la base de datos el usuario
        seleccionado en la aplicacion.
        """
        cursor = self.db.con.cursor()
        sql = "UPDATE usuarios SET nombre = ? WHERE dni = ?"
        data = (nombre, dni)
        cursor.execute(sql, data)
        self.db.con.commit()
        return "actualizar_user"

    def obtener_usuarios(self):
        """
        Metodo que retorna los usuarios existentes ordenados
        por dni.
        """
        cursor = self.db.con.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY dni ASC")
        return cursor.fetchall()
