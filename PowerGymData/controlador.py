from tkinter import Tk
import vista


class Main:
    """
    Función principal para iniciar la interfaz gráfica.
    """
    if __name__ == "__main__":
        try:
            root_tk = Tk()
            vista.Ventana(root_tk, "img.jpg")
            root_tk.mainloop()
        except Exception as e:
            print(f"Error al iniciar Tkinter: {e}")

