import json, csv, os
from datetime import datetime
from livre import Livre
from membre import Membre
from exceptions import *
from tkinter import messagebox
class Bibliotheque:
    def __init__(self):
        self.liste_livres = []
        self.liste_membres = []
        self.charger_donnees()
        
        
    def ajouter_livre(self, livre):
        self.liste_livres.append(livre)
        
        
    def supprimer_livre(self, ISBN):
        for livre in self.liste_livres:
            if livre.ISBN == ISBN:
                self.liste_livres.remove(livre)
                return True
        return False
    
    
    def ajouter_membre(self, membre):
        self.liste_membres.append(membre)
        
        
        
    def emprunter_livre(self, ISBN, id_membre):
        membre = next((m for m in self.liste_membres if int(m.id) == int(id_membre)), None)
        if not membre:
            raise ValueError(f"Membre avec ID {id_membre} introuvable.")

        livre = next((l for l in self.liste_livres if l.ISBN == ISBN), None)
        if not livre:
            raise ValueError(f"Livre avec ISBN {ISBN} introuvable.")

        if livre.statut != "disponible":
            raise ValueError("Ce livre est déjà emprunté.")

        livre.statut = "emprunté"
        membre.livres_empruntes.append(livre)
        self._log_action(ISBN, id_membre, "emprunt")
        
        
        
    def rendre_livre(self, ISBN, id_membre):
        membre = next((m for m in self.liste_membres if int(m.id) == int(id_membre)), None)
        if not membre:
            raise ValueError(f"Membre avec ID {id_membre} introuvable.")

        livre = next((l for l in membre.livres_empruntes if l.ISBN == ISBN), None)
        if not livre:
            raise ValueError("Ce membre n’a pas emprunté ce livre.")

        livre_original = next((l for l in self.liste_livres if l.ISBN == ISBN), None)
        if livre_original:
            livre_original.statut = "disponible"

        membre.livres_empruntes.remove(livre)
        self._log_action(ISBN, id_membre, "retour")       
                
    def sauvegarder_donnees(self):
        with open("data/livres.json","w") as f :
            json.dump([livre.__dict__ for livre in self.liste_livres], f, indent=2)
        with open("data/membres.json","w") as f:
            json.dump([{"id": m.id,
                        "nom": m.nom,
                        "livres_empruntes": [l.ISBN for l in m.livres_empruntes]
                        }for m in self.liste_membres
                       ],f, indent=2)
            
            
    def charger_donnees(self):
        self.liste_livres = []
        if os.path.exists("data/livres.json"):
            try:
                with open("data/livres.json", "r") as f:
                    livres_data = json.load(f)
                    self.liste_livres = [Livre(**livre) for livre in livres_data]
            except json.JSONDecodeError:
                print("Erreur de décodage JSON dans livres.json")
        else:
            print("Fichier livres.json non trouvé, initialisation de la liste des livres vide.")
        self.liste_membres = []
        if os.path.exists("data/membres.json"):
            try:
                with open("data/membres.json", "r") as f:
                    membres_data = json.load(f)
                    for m in membres_data:
                        membre = Membre(m["id"], m["nom"])
                        for isbn in m.get("livres_empruntes", []):
                            livre = next((l for l in self.liste_livres if l.ISBN == isbn), None)
                            if livre:
                                membre.livres_empruntes.append(livre)
                        self.liste_membres.append(membre)
            except json.JSONDecodeError:
                print("Erreur de décodage JSON dans membres.json")
        else:
            print("Fichier membres.json non trouvé, initialisation de la liste des membres vide.")
                
    def _log_action(self, ISBN, id, action):
        with open("data/log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), ISBN, id, action])
            
    def afficher_livres(self):
        for livre in self.liste_livres:
            livre.afficher_livre()