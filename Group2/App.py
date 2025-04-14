import tkinter as tk


def iniciar():
    print("Ejecutado papu uwu")


ventana = tk.Tk()
ventana.title("Group 2 Exercise")
top_frame = tk.Frame(ventana, bg="#f9d4db", height=100)
top_frame.pack(fill=tk.X)

# Crear el botón Iniciar
boton_iniciar = tk.Button(top_frame, text="Iniciar",
                          bg="#ff9690", fg="white", command=iniciar)
boton_iniciar.pack(pady=20)

ventana.mainloop()
