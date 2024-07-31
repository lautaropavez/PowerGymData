from tkinter import StringVar, Label, Entry, ttk, Button, W, E, IntVar, Toplevel
from tkinter.messagebox import showwarning
import os
from PIL import ImageTk, Image
from modelo import GestorUsuarios


# ##############################################
# VISTA
# ##############################################

class Ventana:
    """
    Clase que contiene la parte visual de la aplicacion,
    el cual sera utilizado por el usuario para sus registros.
    """

    def __init__(self, root, icono):
        self.modelo = GestorUsuarios()
        self.tree = ttk.Treeview(root)
        self.actualizar_treeview(self.tree)
        self.root = root
        self.icono_pantalla(icono)
        root.title("Gimnasio")

        # Defino variables para tomar valores de campos de entrada
        titulo = Label(root, text="Ingrese sus datos", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
        titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W + E)

        dni = Label(root, text="DNI", )
        dni.grid(row=1, column=0, sticky=W)
        nombre = Label(root, text="Nombre", )
        nombre.grid(row=2, column=0, sticky=W)
        edad = Label(root, text="Edad", )
        edad.grid(row=3, column=0, sticky=W)
        nacionalidad = Label(root, text="Nacionalidad", )
        nacionalidad.grid(row=4, column=0, sticky=W)
        altura = Label(root, text="Altura(cm)", )
        altura.grid(row=5, column=0, sticky=W)
        peso = Label(root, text="Peso(kg)", )
        peso.grid(row=6, column=0, sticky=W)
        telefono = Label(root, text="telefono", )
        telefono.grid(row=7, column=0, sticky=W)

        dni_var, nombre_var, edad_var, nacionalidad_var, altura_var, peso_var, telefono_var = IntVar(), StringVar(), IntVar(), StringVar(), IntVar(), IntVar(), IntVar()
        w_ancho = 20

        entry_dni = Entry(root, textvariable=dni_var, width=w_ancho)
        entry_dni.grid(row=1, column=1)
        entry_nombre = Entry(root, textvariable=nombre_var, width=w_ancho)
        entry_nombre.grid(row=2, column=1)
        entry_edad = Entry(root, textvariable=edad_var, width=w_ancho)
        entry_edad.grid(row=3, column=1)
        entry_nacionalidad = Entry(root, textvariable=nacionalidad_var, width=w_ancho)
        entry_nacionalidad.grid(row=4, column=1)
        entry_altura = Entry(root, textvariable=altura_var, width=w_ancho)
        entry_altura.grid(row=5, column=1)
        entry_peso = Entry(root, textvariable=peso_var, width=w_ancho)
        entry_peso.grid(row=6, column=1)
        entry_telefono = Entry(root, textvariable=telefono_var, width=w_ancho)
        entry_telefono.grid(row=7, column=1)

        # ##############################################
        # TREEVIEW
        # ##############################################

        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=120, minwidth=50, anchor=W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=20, minwidth=80)
        self.tree.column("col3", width=160, minwidth=80)
        self.tree.column("col4", width=40, minwidth=80)
        self.tree.column("col5", width=40, minwidth=80)
        self.tree.column("col6", width=160, minwidth=80)
        self.tree.heading("#0", text="DNI")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Edad")
        self.tree.heading("col3", text="Nacionalidad")
        self.tree.heading("col4", text="Altura")
        self.tree.heading("col5", text="Peso")
        self.tree.heading("col6", text="Telefono")
        self.tree.grid(column=0, row=12, columnspan=3)

        # ======================================================
        # ===================== BOTONES ========================
        # ======================================================
        boton_alta = Button(root, text="Guardar",
                            command=lambda: self.vista_alta(dni_var, nombre_var, edad_var, nacionalidad_var, altura_var,
                                                            peso_var, telefono_var, self.tree))
        boton_alta.grid(row=8, column=1)
        boton_baja = Button(root, text="Borrar", command=lambda: self.vista_borrar(self.tree))
        boton_baja.grid(row=9, column=1)
        boton_modificar = Button(root, text="Modificar", command=lambda: self.actualizar_usuario(self.tree))
        boton_modificar.grid(row=11, column=1)

    # ======================================================
    # ===================== METODOS ========================
    # ======================================================

    def vista_alta(self, dni_var, nombre_var, edad_var, nacionalidad_var, altura_var, peso_var, telefono_var, tree):
        """
        Metodo que administra el alta del usuario y actualiza la
        aplicacion en caso de ser exitosa.
        """
        try:
            if self.modelo.alta(dni_var.get(), nombre_var.get(), edad_var.get(), nacionalidad_var.get(),
                                altura_var.get(), peso_var.get(), telefono_var.get()):
                print("Usuario agregado correctamente.")
                self.actualizar_treeview(tree)
        except Exception as e:
            print(f"Error al agregar usuario. {e}")

    def vista_borrar(self, tree):
        """
        Metodo que administra la baja del usuario seleccionado
        y actualiza la aplicacion.
        """
        valor = tree.selection()
        if valor:
            dni = tree.item(valor, "text")
            exito = self.modelo.borrar(dni)
            if exito:
                print("Borrado exitoso")
                tree.delete(valor)
                self.actualizar_treeview(tree)
            else:
                print("Error al borrar el usuario.")
        else:
            print("Seleccione un item.")

    def actualizar_usuario(self, tree):
        """
        Metodo encargado de verificar si se selecciono un usuario
        y abrir una ventana para cargar un nuevo nombre.
        """
        valor = tree.selection()
        if not valor:
            showwarning("Advertencia", "Por favor, selecciona un usuario para actualizar.")
            return

        mi_id = tree.item(valor, "text")

        ventana_actualizar = Toplevel()
        ventana_actualizar.title("Actualizar Usuario")

        nueva_etiqueta = Label(ventana_actualizar, text="Nuevo Nombre:")
        nueva_etiqueta.grid(row=0, column=0, padx=10, pady=10)

        nuevo_nombre_var = StringVar()
        nuevo_nombre_entrada = Entry(ventana_actualizar, textvariable=nuevo_nombre_var)
        nuevo_nombre_entrada.grid(row=0, column=1, padx=10, pady=10)

        boton_actualizar = Button(ventana_actualizar, text="Actualizar",
                                  command=lambda: self.realizar_actualizacion(tree, mi_id, nuevo_nombre_var,
                                                                              ventana_actualizar))
        boton_actualizar.grid(row=1, column=0, columnspan=2, pady=10)

        ventana_actualizar.mainloop()

    def realizar_actualizacion(self, tree, mi_id, nuevo_nombre_var, ventana_actualizar):
        """
        Metodo encargado de gestionar la modificacion del usuario
        y la actualizacion de la tabla en la aplicacion.
        """
        nuevo_nombre = nuevo_nombre_var.get()

        try:
            self.modelo.actualizar_user(nuevo_nombre, mi_id)
            self.actualizar_treeview(tree)
            ventana_actualizar.destroy()

        except Exception as e:
            showwarning("Error", f"Error al actualizar: {e}")

    def actualizar_treeview(self, tree):
        """
        Metodo encargado de actualizar los usuarios existentes en
        la aplicacion.
        """
        usuarios = self.modelo.obtener_usuarios()

        records = tree.get_children()
        for element in records:
            tree.delete(element)

        for usuario in usuarios:
            tree.insert("", "end", text=usuario[0],
                        values=(usuario[1], usuario[2], usuario[3], usuario[4], usuario[5], usuario[6]))

    def icono_pantalla(self, icono):
        """
        Metodo encargado de traer a la aplicacion el logo
        y mostrarlo en la misma.
        """
        BASE_DIR = "./"
        ruta = os.path.join(BASE_DIR, "img", icono)
        self.imagen_icono = ImageTk.PhotoImage(
            Image.open(ruta))  # La imagen se guarda como un atributo del objeto Ventana.
        self.root.iconphoto(True, self.imagen_icono)

