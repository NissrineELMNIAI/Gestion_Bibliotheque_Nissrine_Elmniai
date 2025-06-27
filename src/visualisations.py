import matplotlib.pyplot as plt
import json
from collections import Counter
from datetime import datetime, timedelta

def stats_genre():
    try:
        with open("data/livres.json", "r") as f:
            livres_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Le fichier des livres n'existe pas ou est vide.")
        return
    genres = {}
    for livre in livres_data:
        genre = livre["genre"]
        genres[genre] = genres.get(genre, 0) + 1
    
    if genres:
        plt.figure()
        plt.pie(genres.values(), labels = genres.keys(), autopct = "%1.1f%%")
        plt.title("Répartition des livres par genre")
        plt.draw()
        manager = plt.get_current_fig_manager()
        window = manager.window
        centrer_stats(window, 600, 500)
        plt.show()
    else:
        print("Aucun livre trouvé pour générer les statistiques par genre.")


def stats_auteurs():
    with open("data/livres.json","r") as f:
        livres = json.load(f)
    
    auteurs = [livre["auteur"]for livre in livres]
    compteur = Counter(auteurs).most_common(10)
    
    noms, quantites = zip(*compteur) if compteur else ([], [])
    
    plt.figure()
    plt.barh(noms[::-1], quantites[::-1], color="skyblue")
    plt.title("Top 10 des auteurs les plus populaires")
    plt.draw()
    manager = plt.get_current_fig_manager()
    window = manager.window
    centrer_stats(window, 600, 500)
    plt.xlabel("Nombre de livres")
    plt.tight_layout()
    plt.show()


def stats_emprunts():
    activite = {}
    with open("data/historique.csv", "r") as f:
        next(f)
        for ligne in f :
            date_str, _, _, action = ligne.strip().split(";")
            if action == "emprunt" :
                date = datetime.fromisoformat(date_str).date()
                if date >= datetime.today().date() - timedelta(days = 30):
                    activite[date] = activite.get(date, 0)+1
    
    jours = [datetime.today().date() - timedelta(days = i) for i in reversed(range(30))]
    valeurs = [activite.get(j, 0) for j in jours]
    
    plt.figure()
    plt.plot(jours, valeurs, marker="o", color="green")
    plt.title("Activite des emprunts (30 derniers jours)")
    plt.draw()
    manager = plt.get_current_fig_manager()
    window = manager.window
    centrer_stats(window, 600, 500)
    plt.xticks(rotation=45)
    plt.ylabel("Nb emprunts")
    plt.tight_layout()
    plt.show()
    
def centrer_stats(fenetre, largeur, hauteur):
    fenetre.update_idletasks()
    ecran_l = fenetre.winfo_screenwidth()
    ecran_h = fenetre.winfo_screenheight()
    pos_x = int((ecran_l - largeur) / 2) 
    pos_y = int((ecran_h - hauteur) / 2)
    fenetre.geometry(f"{largeur}x{hauteur}+{pos_x}+{pos_y}")
    fenetre.resizable(False, False)
            