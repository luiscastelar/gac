import tkinter as tk
from tkinter import ttk

class CRUD:
    def __init__(self):
        # Inicio el panel raíz (root)
        self.root = tk.Tk()
        self.root.title("Ventana Principal")

        # Inicio del panel principal
        self.create_index_widget()  

    def create_index_widget(self):
        # Borramos todo lo anterior
        self.clear_widgets()

        # Botones en la ventana principal para abrir las ventanas hijas
%%BOTONES%%

        # Acciones de los botones (funciones callback)
%%ACCIONES_DE_BOTONES%%


    def clear_widgets(self):
        # Borramos los widgtes ya ubicados en root
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def run(self):
        # Comenzamos GUI de la App
        self.root.mainloop()


# Check if the script is run directly (not imported)
if __name__ == "__main__":
    # Instanciamos la aplicación
    app = CRUD()
    # La lanzamos
    app.run()
