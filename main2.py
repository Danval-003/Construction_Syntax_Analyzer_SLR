import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
from GUI_funtions import eval_Text, getTotal, create_mach


def get_tag_from_token(token):
    return token  # Usa directamente el token como nombre de etiqueta


class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple IDE")

        # Configurar el área de texto
        self.text_area = tk.Text(root, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        # Configurar la barra de menú
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Crear Maquina", command=self.create_Machine)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=root.quit)

        # Configurar el temporizador de autoguardado
        self.autosave_interval = 10  # segundos
        self.autosave_thread = threading.Thread(target=self.autosave_loop, daemon=True)
        self.autosave_thread.start()

        # Configurar el resaltado
        self.text_area.tag_configure("LET", foreground="green")  # Ajusta según tus necesidades
        self.text_area.tag_configure(1, foreground="red")
        self.text_area.tag_configure(0, foreground="black")
        self.text_area.tag_configure("VARIABLE", foreground="orange")  # Ajusta según tus necesidades
        self.text_area.tag_configure("COMMENTARY", foreground="gray")  # Ajusta según tus necesidades
        self.text_area.tag_configure("RULES", foreground="pink")
        self.text_area.tag_configure("TOKEN", foreground="#87CEEB")
        self.text_area.tag_configure("RETURN", foreground="#630b57")
        self.text_area.tag_configure("SYMBOL", foreground="#87CEEB")
        self.text_area.tag_configure("SYM", foreground="#000080")
        self.text_area.tag_configure("IND", foreground="#000080")
        self.text_area.tag_configure("GROUP", foreground="#000080")

        # Vincular el evento de edición a la función de resaltado
        self.text_area.bind("<KeyRelease>", self.resaltar_ocurrencias)

    def autosave_loop(self):
        while True:
            time.sleep(self.autosave_interval)
            self.save_file(autosave=True)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.root.title("Nuevo Archivo - Simple IDE")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"),
                                                                                   ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.root.title(f"{file_path} - Simple IDE")

    def create_Machine(self):
        print(getTotal())

        for _, tag, _ in self.text_area.dump(1.0, tk.END, tag = 1):
            if tag == '1':
                messagebox.showerror("Error",
                                     f"Error, el archivo contiene errores en la escritura")
                return None
        print(self.text_area.dump(1.0, tk.END, tag = 1))

        if getTotal() > 0:
            create_mach()
        else:
            messagebox.showerror("Error",
                                 f"Error, el archivo contiene errores o no devuelve tokens, por lo que no se puede crear maquina")

    def save_file(self, autosave=False):
        if autosave:
            file_path = "autosave.txt"
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"),
                                                                                         ("Todos los archivos", "*.*")])
            if not file_path:
                return

        with open(file_path, "w") as file:
            file.write(self.text_area.get(1.0, tk.END))
        self.root.title(f"{file_path} - Simple IDE")

    def resaltar_ocurrencias(self, event):
        content = self.text_area.get(1.0, tk.END)
        tokens = eval_Text(content)
        self.text_area.tag_remove("LET", 1.0, tk.END)
        self.text_area.tag_remove(1, 1.0, tk.END)
        self.text_area.tag_remove(0, 1.0, tk.END)
        self.text_area.tag_remove("VARIABLE", 1.0, tk.END)
        self.text_area.tag_remove("COMMENTARY", 1.0, tk.END)
        self.text_area.tag_remove("RULES", 1.0, tk.END)
        self.text_area.tag_remove("TOKEN", 1.0, tk.END)
        self.text_area.tag_remove("RETURN", 1.0, tk.END)
        self.text_area.tag_remove("SYMBOL", 1.0, tk.END)
        self.text_area.tag_remove("SYM", 1.0, tk.END)
        self.text_area.tag_remove("IND", 1.0, tk.END)
        self.text_area.tag_remove("GROUP", 1.0, tk.END)

        start_index = 1.0
        for message, token in tokens:
            end_index = f"{start_index}+{len(message)}c"
            tag = get_tag_from_token(token)
            self.text_area.tag_add(tag, start_index, end_index)
            start_index = end_index


if __name__ == "__main__":
    rooted = tk.Tk()
    ide = SimpleIDE(rooted)
    rooted.geometry("800x600")
    rooted.mainloop()
