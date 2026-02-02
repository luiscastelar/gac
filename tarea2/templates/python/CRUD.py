import tkinter as tk
from tkinter import Toplevel
from functools import partial

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ventana Principal")
ventana_principal.geometry("200x%%ALTURA%%")


# Botón en la ventana principal para abrir la ventana hija
%%BOTONES%%


# Iniciar el loop principal
ventana_principal.mainloop()