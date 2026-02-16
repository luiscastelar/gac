import tkinter as tk
from tkinter import messagebox

class CRUD:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Ventana Principal")
        #self.root.geometry("200x%%ALTURA%%")
        self.create_index_widget()  # Start with the login widgets

    def create_index_widget(self):
        # Create the login and registration widgets
        self.clear_widgets()

        # Botón en la ventana principal para abrir la ventana hija
%%BOTONES%%

        # Acciones de los botones
%%ACCIONES_DE_BOTONES%%


    def clear_widgets(self):
        # Remove all widgets from the root window
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def run(self):
        # Start the Tkinter main loop
        self.root.mainloop()


# Check if the script is run directly (not imported)
if __name__ == "__main__":
    # Create an instance of CRUD
    app = CRUD()
    # Run the application
    app.run()
