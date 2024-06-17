import tkinter.messagebox
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import re

bgColor = "#00c9a7"
prColor = "#12192c"
prLightColor = "#c4fff3"
textHolderColor = "#7a7e89"


# validation fonction
def valider_donnees(nom, tel, email):
    # Vérification du nom (au moins 2 lettres alphabétiques)
    if not re.match(r'^[a-zA-Z\s]{2,}$', nom):
        if len(nom) == 0:
            messagebox.showerror("Erreur", "Le nom est obligatoire.")
        else:
            messagebox.showerror("Erreur", "Le nom doit contenir au moins 2 lettres alphabétiques.")
        return False

    # Vérification du téléphone (10 chiffres commençant par 06, 07 ou 05)
    if not re.match(r'^(06|07|05)\d{8}$', tel):
        if len(tel) == 0:
            messagebox.showerror("Erreur", "Le numéro de téléphone est obligatoire.")
        else:
            messagebox.showerror("Erreur",
                                 "Le numéro de téléphone doit contenir 10 chiffres et commencer par 06, 07 ou 05.")
        return False

    # Vérification de l'email (format email)
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        if len(email) == 0:
            messagebox.showerror("Erreur", "L'email est obligatoire.")
        else:
            messagebox.showerror("Erreur", "L'email doit être valide.")
        return False

    return True


def clearPage(root):
    for widget in root.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()


class AfficherAdherents():
    def __init__(self, root):
        self.root = root
        self.root.config(bg=bgColor)
        self.root.title("Bibliothèque - Afficher les Adherents")

        # content frame
        self.contentframe = Frame(self.root, bg=bgColor, padx=50, pady=50)
        self.contentframe.pack(expand=True, fill="both")
        self.afficherTable()

        # style

        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="white",
                             font=('Rubik', 10))

        self.style.configure("Custom.Treeview.Heading",
                             background="red",
                             foreground="black",
                             font=('Rubik', 11))

        self.style.map('Custom.Treeview',
                       background=[('selected', bgColor)],
                       foreground=[('selected', 'white')])

    def afficherTable(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="bibliotheque")

        cursor = connection.cursor()
        cursor.execute(f"Select * from adherent")
        data = cursor.fetchall()
        columns = ('ID', 'Nom', 'Telephone', 'Email')
        self.tree = ttk.Treeview(self.contentframe, columns=columns, show="headings", style="Custom.Treeview")
        self.tree.tag_configure("oddrow", background="lightblue")

        # Create a scrollbar
        self.tree_scroll = ttk.Scrollbar(self.tree)
        self.tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.trierColumn(self.tree, _col, False))
            self.tree.column(col, width=100, stretch=True)

        for i, item in enumerate(data):
            self.tree.insert("", "end", values=item, tags=("oddrow" if i % 2 == 1 else ""))

        self.tree.pack(fill="both", expand=True)
        cursor.close()
        connection.close()
        self.rechercheAdherent(self.tree)

    def trierColumn(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]

        # Sort the list
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)

        # Reorder items in the treeview
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        for i, child in enumerate(self.tree.get_children('')):
            if i % 2 == 0:
                self.tree.item(child, tags=("oddrow",))
            else:
                self.tree.item(child, tags=())

        treeview.heading(col, text=col, command=lambda: self.trierColumn(treeview, col, not reverse))

    def rechercheAdherent(self, tree):
        search_frame = Frame(self.contentframe, bg=bgColor)
        search_frame.pack(fill="x", padx=5, pady=5)

        search_label = Label(search_frame, text="Search:", bg=bgColor, font=('Rubik', 12))
        search_label.pack(side="left")

        search_entry = Entry(search_frame, font=('Rubik', 11))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        def search_tree():
            query = search_entry.get()
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="bibliotheque")

            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM adherent WHERE CONCAT_WS('', {'idAdh,nom,tel,email'}) LIKE %s",
                           ('%' + query + '%',))
            data = cursor.fetchall()

            tree.delete(*tree.get_children())
            for i in range(len(data)):
                item = data[i]
                self.tree.insert("", "end", values=item, tags=("oddrow" if i % 2 == 1 else ""))

        search_button = Button(search_frame, text="Search", command=search_tree, font=('Rubik', 12), bg=prColor,
                               relief="solid", cursor="hand2", fg="white", activebackground=bgColor,
                               activeforeground="black")
        search_button.pack(side="right")


class AjouterAdherent():
    def __init__(self, root):
        self.root = root
        self.root.config(bg=bgColor)
        self.root.title("Bibliothèque - Ajouter Adherent")

        # content frame
        self.contentframe = Frame(self.root, bg=bgColor)
        self.contentframe.pack(expand=True, fill="both")

        # image
        self.ajouteimage = PhotoImage(file="ajouter_adherent.png")
        self.labelImage = Label(self.contentframe, image=self.ajouteimage, border=0)
        self.labelImage.image = self.ajouteimage
        self.labelImage.place(x=0, y=0)

        self.frame = Frame(self.contentframe, width=350, height=350, bg=bgColor)
        self.frame.place(x=520, y=90)

        self.form_options = Frame(self.frame, bg=bgColor, height=300, width=300)
        self.form_options.pack(padx=10, pady=10)

        # title
        self.title = Label(self.form_options, text="Ajouter adherent", fg=prColor, font=('Rubik', 23), bg=bgColor)
        self.title.grid(row=0, column=0, columnspan=3, rowspan=2, padx=10, pady=10, sticky="e")

        # nom entry
        self.nom_label = Label(self.form_options, text="Nom:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        self.nom_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nom_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                               highlightcolor="black", relief="solid")
        self.nom_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # telephone entry
        self.tel_label = Label(self.form_options, text="Telephone:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        self.tel_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.tel_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                               highlightcolor="black", relief="solid")
        self.tel_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Email entry
        self.email_label = Label(self.form_options, text="Email:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        self.email_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                                 highlightcolor="black", relief="solid")
        self.email_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.modify_button = Button(self.form_options, width=16, text="Ajouter Adherent", bg=bgColor, fg=prColor,
                                    relief="solid",
                                    font=('Rubik', 12), cursor="hand2", activebackground=prColor,
                                    activeforeground=bgColor,
                                    pady=5, command=self.ajouter_adherent)
        self.modify_button.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

    def ajouter_adherent(self):
        tel = self.tel_entry.get().strip()
        nom = self.nom_entry.get().strip()
        email = self.email_entry.get().strip()

        if valider_donnees(nom, tel, email):
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="bibliotheque")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Adherent (nom,  tel, email) VALUES (%s, %s, %s)",
                           (nom, tel, email))
            connection.commit()
            messagebox.showinfo("Success", "l'adherent a été ajouté avec succés")
            clearPage(self.root)
            AfficherAdherents(self.root)


class ModifierAdherent():
    def __init__(self, root):
        self.root = root
        self.root.config(bg=bgColor)
        self.root.title("Bibliothèque - Modifier Adherent")

        # style

        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="white",
                             font=('Rubik', 10))

        self.style.configure("Custom.Treeview.Heading",
                             background="red",
                             foreground="black",
                             font=('Rubik', 12))

        self.style.map('Custom.Treeview',
                       background=[('selected', bgColor)],
                       foreground=[('selected', 'white')])

        # content frame
        self.contentframe = Frame(self.root, bg=bgColor, padx=50, pady=50)
        self.contentframe.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(self.contentframe, columns=('ID', 'Nom', 'Telephone', 'Email'),
                                 show="headings", style="Custom.Treeview")

        # Create a scrollbar
        self.tree_scroll = ttk.Scrollbar(self.tree)
        self.tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.config(command=self.tree.yview)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.trierColumn(self.tree, _col, False))
            self.tree.column(col, width=100, stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.selecterCol)
        self.tree.tag_configure("oddrow", background="lightblue")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.form_options = Frame(self.contentframe, bg=bgColor, height=300)
        self.form_options.pack(fill="x", padx=10, pady=10)

        # nom adherent entry
        self.nom_label = Label(self.form_options, text="Nom:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        self.nom_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.nom_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                               highlightcolor="black", relief="solid")
        self.nom_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # telephone entry
        self.tel_label = Label(self.form_options, text="Telephone:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        self.tel_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.tel_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                               highlightcolor="black", relief="solid")
        self.tel_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # email entry
        email_label = Label(self.form_options, text="Email:", bg=bgColor, fg=prColor, font=('Rubik', 12))
        email_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = Entry(self.form_options, font=('Rubik', 12), fg=prColor, bg="lightblue", border=1,
                                 highlightcolor="black", relief="solid")
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.modify_button = Button(self.form_options, width=17, text="Modifier Adherent", bg=bgColor, fg=prColor,
                                    relief="solid",
                                    font=('Rubik', 12), cursor="hand2", activebackground=prColor,
                                    activeforeground=bgColor,
                                    pady=5, command=self.modifier_adherent)
        self.modify_button.grid(row=0, column=4, columnspan=2, padx=10, pady=10)

        self.supprimer_button = Button(self.form_options, width=17, text="Supprimer Adherent", bg="#e74c3c", fg=prColor,
                                       relief="solid",
                                       font=('Rubik', 12), cursor="hand2", activebackground=prColor,
                                       activeforeground=bgColor,
                                       pady=5, command=self.supprimer_adherent)
        self.supprimer_button.grid(row=1, column=4, columnspan=2, padx=10, pady=10)

        self.afficherInfo()

    def afficherInfo(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="bibliotheque")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM adherent")
        data = cursor.fetchall()
        for i in range(len(data)):
            item = data[i]
            self.tree.insert("", "end", values=item, tags=("oddrow" if i % 2 == 1 else ""))

    def modifier_adherent(self):
        if not self.tree.selection():
            tkinter.messagebox.showwarning("invalid choix", "veuillez selectionner une Adherent!")
            return
        nom = self.nom_entry.get().strip()
        tel = self.tel_entry.get().strip()
        email = self.email_entry.get().strip()
        if valider_donnees(nom, tel, email):
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="bibliotheque")
            cursor = connection.cursor()
            cursor.execute("UPDATE adherent SET nom=%s, tel=%s, email=%s WHERE idAdh=%s",
                           (nom, tel, email, self.selected_adherent_id))
            connection.commit()
            messagebox.showinfo("Success", "l'adherent a été modifier avec succés")
            self.afficherInfo()
            clearPage(self.root)
            self.nom_entry.delete(0, END)
            self.tel_entry.delete(0, END)
            self.email_entry.delete(0, END)


    def supprimer_adherent(self):
        try:
            if not self.tree.selection():
                tkinter.messagebox.showwarning("invalid choix", "veuillez selectionner une adherent!")
                return
            selected_item = self.tree.selection()
            if selected_item:
                response = messagebox.askyesno("Confirm", "Êtes vous sure de supprimer cette adherent?")

                if response:
                    connection = mysql.connector.connect(host="localhost", user="root", password="",
                                                         database="bibliotheque")
                    cursor = connection.cursor()

                    cursor.execute("DELETE FROM Adherent WHERE idAdh=%s", (self.selected_adherent_id,))
                    connection.commit()
                    messagebox.showinfo("Success", "Adherent a été supprimé avec succée")
                    self.afficherInfo()
                    self.nom_entry.delete(0, END)
                    self.tel_entry.delete(0, END)
                    self.email_entry.delete(0, END)
        except:
            messagebox.showerror("Erreur", "vous ne pouvez pas supprimer cet adherent, cet adherent a déja un emprunt")

    def selecterCol(self, event):
        if not self.tree.selection():
            self.nom_entry.delete(0, END)
            self.tel_entry.delete(0, END)
            self.email_entry.delete(0, END)
            return
        selected_item = self.tree.selection()[0]
        selected_values = self.tree.item(selected_item, "values")

        self.selected_adherent_id = selected_values[0]
        self.nom_entry.delete(0, END)
        self.nom_entry.insert(0, selected_values[1])
        self.tel_entry.delete(0, END)
        self.tel_entry.insert(0, selected_values[2])
        self.email_entry.delete(0, END)
        self.email_entry.insert(0, selected_values[3])

    def trierColumn(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]

        # Sort the list
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0], reverse=reverse)

        # Reorder items in the treeview
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        for i, child in enumerate(self.tree.get_children('')):
            if i % 2 == 0:
                self.tree.item(child, tags=("oddrow",))
            else:
                self.tree.item(child, tags=())

        treeview.heading(col, text=col, command=lambda: self.trierColumn(treeview, col, not reverse))
