import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from datetime import datetime

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bibliotheque"
)


# Main Application Class
class LibraryManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.configure(background="#f0f0f0")

        self.font_style = font.Font(family="Rubik", size=11)

        self.menu = tk.Menu(self, font=self.font_style)
        self.config(menu=self.menu)

        self.livre_menu = tk.Menu(self.menu, tearoff=0, font=self.font_style)
        self.adherent_menu = tk.Menu(self.menu, tearoff=0, font=self.font_style)
        self.emprunt_menu = tk.Menu(self.menu, tearoff=0, font=self.font_style)

        self.menu.add_cascade(label="Livre", menu=self.livre_menu)
        self.menu.add_cascade(label="Adherent", menu=self.adherent_menu)
        self.menu.add_cascade(label="Emprunt", menu=self.emprunt_menu)

        self.livre_menu.add_command(label="Lister", command=self.show_livre_list)
        self.livre_menu.add_command(label="Ajouter", command=self.show_add_livre)
        self.livre_menu.add_command(label="Modifier", command=self.show_modify_livre)
        self.livre_menu.add_command(label="Supprimer", command=self.show_delete_livre)

        self.adherent_menu.add_command(label="Lister", command=self.show_adherent_list)
        self.adherent_menu.add_command(label="Ajouter", command=self.show_add_adherent)
        self.adherent_menu.add_command(label="Modifier", command=self.show_modify_adherent)
        self.adherent_menu.add_command(label="Supprimer", command=self.show_delete_adherent)

        self.emprunt_menu.add_command(label="Lister", command=self.show_emprunt_list)
        self.emprunt_menu.add_command(label="Ajouter", command=self.show_add_emprunt)
        self.emprunt_menu.add_command(label="Modifier", command=self.show_modify_emprunt)

        self.content_frame = tk.Frame(self, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True)

        self.show_livre_list()

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_livre_list(self):
        self.clear_frame()
        self.show_table("Livre")

    def show_add_livre(self):
        self.clear_frame()
        AddLivreForm(self.content_frame).pack(fill="both", expand=True)

    def show_modify_livre(self):
        self.clear_frame()
        ModifyLivreForm(self.content_frame).pack(fill="both", expand=True)

    def show_delete_livre(self):
        self.clear_frame()
        DeleteLivreForm(self.content_frame).pack(fill="both", expand=True)

    def show_adherent_list(self):
        self.clear_frame()
        self.show_table("Adherent")

    def show_add_adherent(self):
        self.clear_frame()
        AddAdherentForm(self.content_frame).pack(fill="both", expand=True)

    def show_modify_adherent(self):
        self.clear_frame()
        ModifyAdherentForm(self.content_frame).pack(fill="both", expand=True)

    def show_delete_adherent(self):
        self.clear_frame()
        DeleteAdherentForm(self.content_frame).pack(fill="both", expand=True)

    def show_emprunt_list(self):
        self.clear_frame()
        self.show_table("Emprunt")

    def show_add_emprunt(self):
        self.clear_frame()
        AddEmpruntForm(self.content_frame).pack(fill="both", expand=True)

    def show_modify_emprunt(self):
        self.clear_frame()
        ModifyEmpruntForm(self.content_frame).pack(fill="both", expand=True)

    def show_table(self, table_name):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(tree, _col, False))
            tree.column(col, width=100, stretch=True)

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
        self.add_search_functionality(tree, table_name)

    def add_search_functionality(self, tree, table_name):
        search_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=5, pady=5)

        search_label = tk.Label(search_frame, text="Search:", bg="#f0f0f0", font=self.font_style)
        search_label.pack(side="left")

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        def search_tree():
            query = search_entry.get()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE CONCAT_WS('', {','.join(tree['columns'])}) LIKE %s",
                           ('%' + query + '%',))
            rows = cursor.fetchall()

            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert("", "end", values=row)

        search_button = tk.Button(search_frame, text="Search", command=search_tree, font=self.font_style)
        search_button.pack(side="right")

    def treeview_sort_column(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        treeview.heading(col, text=col, command=lambda: self.treeview_sort_column(treeview, col, not reverse))


# Form classes
class AddLivreForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Title:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Pages:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(self)
        self.pages_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Author:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self)
        self.author_entry.grid(row=2, column=1, padx=5, pady=5)

        self.available_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Available", variable=self.available_var, bg="#f0f0f0", font=app.font_style).grid(
            row=3, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(self, text="Add Book", command=self.add_book, bg="#4CAF50", fg="white", font=app.font_style).grid(
            row=4, column=0, columnspan=2, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        pages = self.pages_entry.get()
        author = self.author_entry.get()
        available = self.available_var.get()

        cursor = db.cursor()
        cursor.execute("INSERT INTO Livre (titre, pages, nomauteur, disponible) VALUES (%s, %s, %s, %s)",
                       (title, pages, author, available))
        db.commit()
        messagebox.showinfo("Success", "Book added successfully")


class ModifyLivreForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.selected_book_id = None
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("idLiv", "titre", "pages", "nomauteur", "prix", "disponible"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True)

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(form_frame, text="Title:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Pages:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(form_frame)
        self.pages_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Author:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(form_frame)
        self.author_entry.grid(row=2, column=1, padx=5, pady=5)

        self.available_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form_frame, text="Available", variable=self.available_var, bg="#f0f0f0",
                       font=app.font_style).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(self, text="Modify Book", command=self.modify_book, bg="#4CAF50", fg="white",
                  font=app.font_style).pack(pady=10)

        self.populate_tree()

    def populate_tree(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Livre")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        selected_values = self.tree.item(selected_item, "values")

        self.selected_book_id = selected_values[0]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_values[1])
        self.pages_entry.delete(0, tk.END)
        self.pages_entry.insert(0, selected_values[2])
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, selected_values[3])
        self.available_var.set(selected_values[5] == '1')

    def modify_book(self):
        title = self.title_entry.get()
        pages = self.pages_entry.get()
        author = self.author_entry.get()
        available = self.available_var.get()

        cursor = db.cursor()
        cursor.execute("UPDATE Livre SET titre=%s, pages=%s, nomauteur=%s, disponible=%s WHERE idLiv=%s",
                       (title, pages, author, available, self.selected_book_id))
        db.commit()
        messagebox.showinfo("Success", "Book modified successfully")
        self.populate_tree()


class DeleteLivreForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("idLiv", "titre", "pages", "nomauteur", "prix", "disponible"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.populate_tree()

        tk.Button(self, text="Delete Selected Book", command=self.delete_book, bg="#FF5733", fg="white",
                  font=app.font_style).pack(pady=10)

    def populate_tree(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Livre")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_book_id = self.tree.item(selected_item, "values")[0]
            cursor = db.cursor()
            cursor.execute("DELETE FROM Livre WHERE idLiv=%s", (selected_book_id,))
            db.commit()
            messagebox.showinfo("Success", "Book deleted successfully")
            self.populate_tree()


class AddAdherentForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Name:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Telephone:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.tel_entry = tk.Entry(self)
        self.tel_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Email:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Add Adherent", command=self.add_adherent, bg="#4CAF50", fg="white",
                  font=app.font_style).grid(row=3, column=0, columnspan=2, pady=10)

    def add_adherent(self):
        name = self.name_entry.get()
        tel = self.tel_entry.get()
        email = self.email_entry.get()

        cursor = db.cursor()
        cursor.execute("INSERT INTO Adherent (nom, tel, email) VALUES (%s, %s, %s)", (name, tel, email))
        db.commit()
        messagebox.showinfo("Success", "Adherent added successfully")


class ModifyAdherentForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.selected_adherent_id = None
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("idAdh", "nom", "tel", "email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True)

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(form_frame, text="Name:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Telephone:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.tel_entry = tk.Entry(form_frame)
        self.tel_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Modify Adherent", command=self.modify_adherent, bg="#4CAF50", fg="white",
                  font=app.font_style).pack(pady=10)

        self.populate_tree()

    def populate_tree(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Adherent")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        selected_values = self.tree.item(selected_item, "values")

        self.selected_adherent_id = selected_values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, selected_values[1])
        self.tel_entry.delete(0, tk.END)
        self.tel_entry.insert(0, selected_values[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, selected_values[3])

    def modify_adherent(self):
        name = self.name_entry.get()
        tel = self.tel_entry.get()
        email = self.email_entry.get()

        cursor = db.cursor()
        cursor.execute("UPDATE Adherent SET nom=%s, tel=%s, email=%s WHERE idAdh=%s",
                       (name, tel, email, self.selected_adherent_id))
        db.commit()
        messagebox.showinfo("Success", "Adherent modified successfully")
        self.populate_tree()


class DeleteAdherentForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("idAdh", "nom", "tel", "email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.populate_tree()

        tk.Button(self, text="Delete Selected Adherent", command=self.delete_adherent, bg="#FF5733", fg="white",
                  font=app.font_style).pack(pady=10)

    def populate_tree(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Adherent")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def delete_adherent(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_adherent_id = self.tree.item(selected_item, "values")[0]
            cursor = db.cursor()
            cursor.execute("DELETE FROM Adherent WHERE idAdh=%s", (selected_adherent_id,))
            db.commit()
            messagebox.showinfo("Success", "Adherent deleted successfully")
            self.populate_tree()


class AddEmpruntForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Book:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.book_combobox = ttk.Combobox(self)
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Adherent:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.adherent_combobox = ttk.Combobox(self)
        self.adherent_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Date:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(self, text="Status:", bg="#f0f0f0", font=app.font_style).grid(row=3, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(value="Take")
        tk.Radiobutton(self, text="Take", variable=self.status_var, value="Take", bg="#f0f0f0",
                       font=app.font_style).grid(row=3, column=1, padx=5, pady=5)
        tk.Radiobutton(self, text="Return", variable=self.status_var, value="Return", bg="#f0f0f0",
                       font=app.font_style).grid(row=3, column=2, padx=5, pady=5)

        tk.Button(self, text="Add Emprunt", command=self.add_emprunt, bg="#4CAF50", fg="white",
                  font=app.font_style).grid(row=4, column=0, columnspan=3, pady=10)

        self.populate_comboboxes()

    def populate_comboboxes(self):
        cursor = db.cursor()
        cursor.execute("SELECT idLiv, titre FROM Livre")
        books = cursor.fetchall()
        self.book_combobox["values"] = [f"{book[1]} ({book[0]})" for book in books]

        cursor.execute("SELECT idAdh, nom FROM Adherent")
        adherents = cursor.fetchall()
        self.adherent_combobox["values"] = [f"{adherent[1]} ({adherent[0]})" for adherent in adherents]

    def add_emprunt(self):
        book_id = self.book_combobox.get().split('(')[-1][:-1]
        adherent_id = self.adherent_combobox.get().split('(')[-1][:-1]
        date_emprunt = self.date_entry.get()
        status = self.status_var.get() == "Take"

        cursor = db.cursor()
        cursor.execute("INSERT INTO Emprunt (idAdh, idLiv, dateemprunt, status) VALUES (%s, %s, %s, %s)",
                       (adherent_id, book_id, date_emprunt, status))
        db.commit()
        messagebox.showinfo("Success", "Emprunt added successfully")


class ModifyEmpruntForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.selected_emprunt_id = None
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("idEmp", "idAdh", "idLiv", "dateemprunt", "status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True)

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(form_frame, text="Book:", bg="#f0f0f0", font=app.font_style).grid(row=0, column=0, padx=5, pady=5)
        self.book_combobox = ttk.Combobox(form_frame)
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Adherent:", bg="#f0f0f0", font=app.font_style).grid(row=1, column=0, padx=5, pady=5)
        self.adherent_combobox = ttk.Combobox(form_frame)
        self.adherent_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Date:", bg="#f0f0f0", font=app.font_style).grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Status:", bg="#f0f0f0", font=app.font_style).grid(row=3, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar()
        tk.Radiobutton(form_frame, text="Take", variable=self.status_var, value="Take", bg="#f0f0f0",
                       font=app.font_style).grid(row=3, column=1, padx=5, pady=5)
        tk.Radiobutton(form_frame, text="Return", variable=self.status_var, value="Return", bg="#f0f0f0",
                       font=app.font_style).grid(row=3, column=2, padx=5, pady=5)

        tk.Button(form_frame, text="Modify Emprunt", command=self.modify_emprunt, bg="#4CAF50", fg="white",
                  font=app.font_style).grid(row=4, column=0, columnspan=3, pady=10)

        self.populate_comboboxes()

    def populate_comboboxes(self):
        cursor = db.cursor()
        cursor.execute("SELECT idLiv, titre FROM Livre")
        books = cursor.fetchall()
        self.book_combobox["values"] = [f"{book[1]} ({book[0]})" for book in books]

        cursor.execute("SELECT idAdh, nom FROM Adherent")
        adherents = cursor.fetchall()
        self.adherent_combobox["values"] = [f"{adherent[1]} ({adherent[0]})" for adherent in adherents]

    def populate_tree(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Emprunt")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        selected_values = self.tree.item(selected_item, "values")

        self.selected_emprunt_id = selected_values[0]
        self.book_combobox.set(f"{selected_values[2]} ({selected_values[1]})")
        self.adherent_combobox.set(f"{selected_values[1]} ({selected_values[2]})")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_values[3])
        self.status_var.set("Take" if selected_values[4] else "Return")

    def modify_emprunt(self):
        book_id = self.book_combobox.get().split('(')[-1][:-1]
        adherent_id = self.adherent_combobox.get().split('(')[-1][:-1]
        date_emprunt = self.date_entry.get()
        status = self.status_var.get() == "Take"

        cursor = db.cursor()
        cursor.execute("UPDATE Emprunt SET idAdh=%s, idLiv=%s, dateemprunt=%s, status=%s WHERE idEmp=%s",
                       (adherent_id, book_id, date_emprunt, status, self.selected_emprunt_id))
        db.commit()
        messagebox.showinfo("Success", "Emprunt modified successfully")
        self.populate_tree()


if __name__ == "__main__":
    app = LibraryManagementApp()
    app.mainloop()
