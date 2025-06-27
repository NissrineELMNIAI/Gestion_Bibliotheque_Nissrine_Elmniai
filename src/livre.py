class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre, statut):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = statut
    def afficher_livre(self):
        print(f"ISBN: {self.ISBN}, Titre: {self.titre}, Auteur: {self.auteur}, Année: {self.annee}, Genre: {self.genre}, Statut: {self.statut}")