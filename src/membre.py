class Membre:
    def __init__(self , id, nom):
        self.id = id
        self.nom = nom
        self.livres_empruntes = []
    def afficher_membre(self):
        print(f"ID: {self.id}, Nom: {self.nom}, Livres empruntés: {[livre.titre for livre in self.livres_empruntes]}")