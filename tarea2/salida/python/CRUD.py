import tkinter as tk
from tkinter import Toplevel
from functools import partial

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ventana Principal")
ventana_principal.geometry("200x150")


# Botón en la ventana principal para abrir la ventana hija
def abrir_ventana_hija_1(objeto1):
    ventana_hija = Toplevel(ventana_principal)
    ventana_hija.title(title)
    ventana_hija.geometry("250x150")
    
    etiqueta = tk.Label(ventana_hija, text=label, font=("Arial", 12))
    etiqueta.pack(pady=10)

    etiqueta = tk.Label(ventana_hija, text=table, font=("Arial", 12))
    etiqueta.pack(pady=10)
    
    boton_cerrar = tk.Button(ventana_hija, text="Cerrar", command=ventana_hija.destroy)
    boton_cerrar.pack(pady=10)

label = f'Ventana {str(1)}'
table = 'calificaciones'
title = 'Ventana calificaciones'
objeto_1 = label, table, title
boton_abrir_1 = tk.Button(ventana_principal, text="calificaciones", command=partial(abrir_ventana_hija_1, objeto_1))
boton_abrir_1.pack(pady=20)
def abrir_ventana_hija_2(objeto2):
    ventana_hija = Toplevel(ventana_principal)
    ventana_hija.title(title)
    ventana_hija.geometry("250x150")
    
    etiqueta = tk.Label(ventana_hija, text=label, font=("Arial", 12))
    etiqueta.pack(pady=10)

    etiqueta = tk.Label(ventana_hija, text=table, font=("Arial", 12))
    etiqueta.pack(pady=10)
    
    boton_cerrar = tk.Button(ventana_hija, text="Cerrar", command=ventana_hija.destroy)
    boton_cerrar.pack(pady=10)

label = f'Ventana {str(2)}'
table = 'alumnos'
title = 'Ventana alumnos'
objeto_2 = label, table, title
boton_abrir_2 = tk.Button(ventana_principal, text="alumnos", command=partial(abrir_ventana_hija_2, objeto_2))
boton_abrir_2.pack(pady=20)



# Iniciar el loop principal
ventana_principal.mainloop()