import random

class Carte:
    def __init__(self, valeur, couleur):
        if valeur < 1 or valeur > 13:
            raise ValueError("La valeur de la carte doit être entre 1 et 13.")
        if couleur not in ["Coeur", "Carreau", "Trèfle", "Pique"]:
            raise ValueError("Couleur invalide.")
        self.valeur = valeur
        self.couleur = couleur

    def __str__(self):
        noms_valeurs = {1: "As", 11: "Valet", 12: "Dame", 13: "Roi"}
        nom_valeur = noms_valeurs.get(self.valeur, str(self.valeur))
        return f"{nom_valeur} de {self.couleur}"

    def calcule_puissance(self, couleur, tarneeb):
        if self.couleur != couleur and self.couleur != tarneeb:
            return 0
        puissance = self.valeur if self.valeur != 1 else 14
        return puissance * (10 if self.couleur == tarneeb else 1)

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []
        self.score = 0

    def ajouter_carte(self, carte):
        self.main.append(carte)

    def jouer_carte(self, index):
        return self.main.pop(index)

    def afficher_main(self):
        for carte in self.main:
            print(carte)

    def incrementer_score(self):
        self.score += 1

    def choisir_meilleure_carte(self, couleur, tarneeb):
        cartes_de_la_couleur = [
            (carte.calcule_puissance(couleur, tarneeb), index)
            for index, carte in enumerate(self.main)
            if carte.couleur == couleur
        ]
        cartes_du_tarneeb = [
            (carte.calcule_puissance(couleur, tarneeb), index)
            for index, carte in enumerate(self.main)
            if carte.couleur == tarneeb
        ]
        if cartes_de_la_couleur:
            cartes_de_la_couleur.sort()
            return cartes_de_la_couleur[0][1]
        if cartes_du_tarneeb:
            cartes_du_tarneeb.sort()
            return cartes_du_tarneeb[0][1]
        cartes_restantes = [
            (carte.calcule_puissance(couleur, tarneeb), index)
            for index, carte in enumerate(self.main)
        ]
        cartes_restantes.sort()
        return cartes_restantes[0][1]

class TourJeu:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.couleur_du_tour = random.choice(["Coeur", "Carreau", "Trèfle", "Pique"])
        self.tarneeb = random.choice(["Coeur", "Carreau", "Trèfle", "Pique"])
        self.cartes_jouees = {}

    def jouer(self):
        print(f"\nUn nouveau tour commence...")
        print(f" La couleur de ce tour est {self.couleur_du_tour}")
        print(f" Le TARNEEB de ce tour est {self.tarneeb}")
        for joueur in self.joueurs:
            index_carte = joueur.choisir_meilleure_carte(self.couleur_du_tour, self.tarneeb)
            carte_jouee = joueur.jouer_carte(index_carte)
            self.cartes_jouees[joueur] = carte_jouee
            print(f"{joueur.nom} joue {carte_jouee}")
        gagnant = self.evaluer_partie()
        gagnant.incrementer_score()
        print(f"{gagnant.nom} remporte la partie. Son score est maintenant: {gagnant.score}")
        return gagnant

    def evaluer_partie(self):
        puissance_max = -1
        gagnant = None
        for joueur, carte in self.cartes_jouees.items():
            puissance = carte.calcule_puissance(self.couleur_du_tour, self.tarneeb)
            if puissance > puissance_max:
                puissance_max = puissance
                gagnant = joueur
        return gagnant

class PartieJeu:
    def __init__(self, joueurs, n_tours=13):
        self.joueurs = joueurs
        self.historique_tours = []
        self.n_tours = n_tours

    def lancer(self):
        couleurs = ["Coeur", "Carreau", "Trèfle", "Pique"]
        cartes = [Carte(valeur, couleur) for couleur in couleurs for valeur in range(1, 14)]
        random.shuffle(cartes)
        for i, carte in enumerate(cartes):
            self.joueurs[i % len(self.joueurs)].ajouter_carte(carte)
        for _ in range(self.n_tours):
            tour = TourJeu(self.joueurs)
            gagnant = tour.jouer()
            self.historique_tours.append(tour)

    def afficher_resultats(self):
        print("\n---SCORE FINAL---")
        for joueur in self.joueurs:
            print(f"{joueur.nom} - {joueur.score}")
            
joueurs = [Joueur("Charbel"), Joueur("John"), Joueur("Fares"), Joueur("Dagher")]
partie = PartieJeu(joueurs)
partie.lancer()
partie.afficher_resultats()