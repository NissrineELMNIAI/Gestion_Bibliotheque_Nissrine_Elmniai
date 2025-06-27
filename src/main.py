import os
import json
import tkinter as tk
from tkinter import messagebox
from bibliotheque import Bibliotheque
from livre import Livre 
from membre import Membre 
from exceptions import *
from visualisations import stats_genre, stats_auteurs, stats_emprunts

os.makedirs("data", exist_ok=True)
if not os.path.exists("data/livres.json"):
    with open("data/livres.json", "w") as f:
        json.dump({}, f)
    if not os.path.exists("data/membres.json"):
        with open("data/membres.json", "w") as f :
            json.dump({}, f)
    if not os.path.exists("data/historique.csv"):
        with open("data/historique.csv", "w") as f:
            f.write("ISBN,ID,Membre,Date,Action\n")
            

class Main(tk.Tk):
    def __init__(self) :
        super().__init__()
        self.configure(bg="#ffffff")  # Couleur de fond principale
        label_bienvenue = tk.Label(self, text="Bienvenue dans votre bibliothèque", font=("Segoe UI", 14, "bold"), fg="#2c3e50", bg="#f8f8f8")
        label_bienvenue.pack(pady=(15, 5))
        self.style_couleur_fond = "#e8eff1"
        self.style_couleur_texte = "#000000"
        self.style_couleur_bouton = "#4682B4"  # Couleur des boutons
        self.style_couleur_bouton_hover = "#5a9bd5"
        self.style_police = ("Segoe UI", 11, "bold")

        self.option_add("*Font", self.style_police)
        self.option_add("*Background", self.style_couleur_fond)
        self.option_add("*Foreground", self.style_couleur_texte)
        self.option_add("*Button.Background", self.style_couleur_bouton)
        self.option_add("*Button.Foreground", "white")
        self.option_add("*Button.ActiveBackground", self.style_couleur_bouton_hover)
        self.option_add("*Button.ActiveForeground", "white")

        self.title("Systeme des Gestion de Bibliotheque")
        largeur = 400
        hauteur = 400
        
        ecran_largeur = self.winfo_screenwidth()
        ecran_hauteur = self.winfo_screenheight()   
        
        pos_x = int((ecran_largeur / 2) - (largeur / 2))
        pos_y = int((ecran_hauteur / 2) - (hauteur / 2))
        
        self.geometry(f"{largeur}x{hauteur}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.biblio = Bibliotheque()
        
        btn1 = tk.Button(self, text = "Ajouter un livre", command = self.ajouter_livre, width=30)
        btn2 = tk.Button(self, text = "Iscrire un membre", command = self.ajouter_membre, width=30)
        btn3 = tk.Button(self, text = "Emprunter un livre", command = self.emprunter_livre, width=30)
        btn4 = tk.Button(self, text= "Rendre un livre", command = self.rendre_livre, width=30)
        btn5 = tk.Button(self, text = "Afficher les livres", command = self.afficher_livres, width=30)
        btn6 = tk.Button(self, text = "Afficher les statistiques", command = lambda : ouvrir_statistiques(self), width=30)
        btn7 = tk.Button(self, text = "Sauvegarder", command = self.biblio.sauvegarder_donnees, width=17)
        
        for btn in btn1, btn2, btn3, btn4, btn5, btn6, btn7 :
            btn.pack(pady=5)
            
    def ajouter_livre(self):
            win = tk.Toplevel(self)
            win.title("Ajouter un livre")
            centrer_fenetre(win, 300, 300)
            entries = {}
            for champ in ["ISBN", "Titre", "Auteur", "Année", "Genre"]:
                tk.Label(win, text=champ).pack()
                entry = tk.Entry(win)
                entry.pack()
                entries[champ] = entry
                
            def enregistrer():
                livre = Livre(
                    entries["ISBN"].get(),
                    entries["Titre"].get(),
                    entries["Auteur"].get(),
                    int(entries["Année"].get()),
                    entries["Genre"].get(),
                    "disponible"
                )
                self.biblio.ajouter_livre(livre)
                messagebox.showinfo("Succès", "Livre ajouté avec succès !")
                win.destroy()
        
            tk.Button(win, text="Enregistrer", command=enregistrer).pack()
    
    def ajouter_membre(self):
        win = tk.Toplevel(self)
        centrer_fenetre(win, 300, 200)
        win.title("Inscrire un membre")
        tk.Label(win, text="ID").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()
        tk.Label(win, text="Nom").pack()
        nom_entry = tk.Entry(win)
        nom_entry.pack()
        
        def enregistrer():
            membre = Membre(id_entry.get(),nom_entry.get())
            self.biblio.ajouter_membre(membre)
            messagebox.showinfo("Succès", "Membre inscrit !")
            win.destroy()
            
        tk.Button(win, text="Ajouter", command=enregistrer).pack()
        
        self.biblio.charger_donnees()
        self.biblio.sauvegarder_donnees()

    def emprunter_livre(self):
        self._operation_livre("Emprunter")
    def rendre_livre(self):
        self._operation_livre("Rendre")
        
    def _operation_livre(self, action):
        win = tk.Toplevel(self)
        centrer_fenetre(win, 300, 200)
        win.title(f"{action} un livre")
        tk.Label(win, text = "ISBN").pack(pady=(10,0))
        isbn_entry = tk.Entry(win)
        isbn_entry.pack()
        tk.Label(win, text = "ID Membre").pack(pady=(10,0))
        id_entry = tk.Entry(win)
        id_entry.pack()
    
        def executer():
            isbn = isbn_entry.get().strip()
            id_membre = id_entry.get().strip()
            if not isbn or not id_membre:
                messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.")
                return
            try :
                id_membre = int(id_membre)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID du membre doit être un nombre entier.")
                return
            try :
                if action == "Emprunter":
                    self.biblio.emprunter_livre(isbn, id_membre)
                    verbe = "emprunté"
                else :
                    self.biblio.rendre_livre(isbn, id_membre)
                    verbe = "retourné"
                messagebox.showinfo("Succès", f"Livre {action.lower()}é avec succès.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"{type(e).__name__} : {str(e)}")
        
        tk.Button(win, text = f"{action} Livre", command=executer).pack(pady=15)
    def afficher_livres(self):
        win = tk.Toplevel(self)
        centrer_fenetre(win, 300, 300)
        win.title("Liste des livres")
        
        if not self.biblio.liste_livres:
            tk.Label(win, text="Aucun livre trouve").pack(padx=10, pady=10)
            return
        
        for livre in self.biblio.liste_livres:
            desc = f"{livre.ISBN} - {livre.titre} ({livre.auteur}, {livre.annee}) [{livre.genre}] - {livre.statut}"
            tk.Label(win, text=desc, anchor="w", justify="left").pack(fill="x", padx=10, pady=5)
def centrer_fenetre(self, largeur, hauteur):
    ecran_largeur = self.winfo_screenwidth()
    ecran_hauteur = self.winfo_screenheight()
    pos_x = int((ecran_largeur / 2) - (largeur / 2))
    pos_y = int((ecran_hauteur / 2) - (hauteur / 2))
    self.geometry(f"{largeur}x{hauteur}+{pos_x}+{pos_y}")
def ouvrir_statistiques(parent):
    win = tk.Toplevel(parent)
    win.title("Statistiques")
    win.geometry("350x200")
    
    win.update_idletasks()
    largeur, hauteur = 350, 200
    ecranl, ecranh = win.winfo_screenwidth(), win.winfo_screenheight()
    x = int((ecranl / 2) - (largeur / 2))
    y = int((ecranh / 2) - (hauteur / 2))
    win.geometry(f"{largeur}x{hauteur}+{x}+{y}")
    
    btn1 = tk.Button(win, text="Statistiques par genre", command=stats_genre, width=25)
    btn2 = tk.Button(win, text="Top 10 des auteurs", command=stats_auteurs, width=25)
    btn3 = tk.Button(win, text="Statistiques des emprunts", command=stats_emprunts, width=25)
    btn_quit = tk.Button(win, text="Quitter", command=win.destroy, width=10)
    
    btn1.pack(pady=5)
    btn2.pack(pady=5)
    btn3.pack(pady=5)
    btn_quit.pack(pady=10)
    
    
    
        
if __name__ == "__main__":
    app = Main()
    app.mainloop()
