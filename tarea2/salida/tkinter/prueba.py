from tkinter import *
from tkinter import messagebox
import sqlite3

root=Tk()
root.title("Aplicación con B.D")
root.geometry("350x300")

miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miPass=StringVar()
miDireccion=StringVar()

def conexionBBDD():
    

    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    
    try:
        
        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDO VARCHAR(20),
            DIRECCION VARCHAR(50))
            
            ''')
        #COMENTARIOS VARCHAR(100))
        
        
        messagebox.showinfo("BBDD","BBDD creada con éxito")
    
    except:
        
        messagebox.showwarning("¡Atención!","La BBDD ya existe")
    
def salirAplicacion():
    
    valor=messagebox.askquestion("Salir","¿Deseas salir de la aplicación?")
    if valor=="yes":
        root.destroy()
        
def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miApellido.set("")
    miDireccion.set("")
    miPass.set("")
    #textoComentario.delete(1,0,END)
    
    
def mensaje():
    print("pulsaste!")

    
    
def crear():
    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get()
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?)", (datos))
    
    miConexion.commit()
    
    messagebox.showinfo("BBDD","Registro insertado con éxito")

"""  El siguiente codigo favorece sql injection, y es inseguro. Aunque funciona

    def crear():
    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,'"+miNombre.get()+
                     
                     "','" + miPass.get() + 
                     "','" + miApellido.get()+
                     "','" + miDireccion.get() + "')")
                    
    miConexion.commit()
    
    messagebox.showinfo("BBDD","Registro insertado con éxito")
    
"""
    
    
def leer():
    
    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID=" +miId.get())
    elUsuario=miCursor.fetchall()
    
    for usuario in elUsuario:
        
        miId.set(usuario[0])
        miNombre.set(usuario[1])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])
    
    
    miConexion.commit()

    
def actualizar():
    
    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get()
    
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO=?, PASSWORD=?, APELLIDO=?, DIRECCION=? "+
    
    "WHERE ID=" + miId.get(),(datos))
    
    
    
    """" Siguiente codigo susceptible de SQL Inyection
    
    
    miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO='"+miNombre.get()+
        "', PASSWORD='" + miPass.get() + 
        "', APELLIDO='" + miApellido.get() +
        "', DIRECCION='" + miDireccion.get() +
        "' WHERE ID=" + miId.get())
        
    """
    
    miConexion.commit()
    
    messagebox.showinfo("BBDD","Registro actualizado con éxito")
    
    
def borrar():
    
    miConexion=sqlite3.connect("UsuariosDB")
    miCursor=miConexion.cursor()
    miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID=" +miId.get())
                    
    miConexion.commit()
    
    messagebox.showinfo("BBDD","Registro borrado con éxito")
    
    
menubar=Menu(root)
menubasedat=Menu(menubar, tearoff=0)
menubasedat.add_command(label="Conectar", command=conexionBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="BBDD", menu=menubasedat)


menuborrar=Menu(menubar, tearoff=0)
menuborrar.add_command(label="Borrar campos", command=limpiarCampos)
menubar.add_cascade(label="Borrar",menu=menuborrar )

crud=Menu(menubar, tearoff=0)
crud.add_command(label="Añadir", command=crear)
crud.add_command(label="Leer", command=leer)
crud.add_command(label="Actualizar", command=actualizar)
crud.add_command(label="Borrar", command=borrar)
menubar.add_cascade(label="CRUD", menu=crud)


ayudamenu=Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Licencia", command=mensaje)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

root.config(menu=menubar)

l1=Label(root, text="Id: ")
l1.grid(column=0, row=1)


e1=Entry(root, textvariable=miId)
e1.grid(column=1, row=1)

l2=Label(root, text="Nombre: ")
l2.grid(column=0, row=2)


e2=Entry(root, textvariable=miNombre)
e2.grid(column=1, row=2)

l3=Label(root, text="Password: ")
l3.grid(column=0, row=3)

e3=Entry(root,textvariable=miPass)
e3.grid(column=1, row=3)

# textvariable="password", show="*"

l4=Label(root, text="Apellido: ")
l4.grid(column=0, row=4)

e4=Entry(root,textvariable=miApellido)
e4.grid(column=1, row=4)

l5=Label(root, text="Dirección: ")
l5.grid(column=0, row=5)

e5=Entry(root,textvariable=miDireccion)
e5.grid(column=1, row=5)

#l6=Label(root, text="Comentario: ", textvariable=textoComentario)
#l6.grid(column=0, row=6)

#l6=Text(root, width=20, height=6)
#l6.place(x=75,y=110)



b1=Button(root, text="Create", command=crear)
b1.place(x=40,y=250)

b2=Button(root, text="Read", command=leer)
b2.place(x=90,y=250)

b3=Button(root, text="Update", command=actualizar)
b3.place(x=130,y=250)

b4=Button(root, text="Delete", command=borrar)
b4.place(x=180,y=250)

root.mainloop()