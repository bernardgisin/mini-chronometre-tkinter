#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
py0108_chrono.py
Mini chronomètre.
Code généré par Gemini, le 18.2.2026
'''
import tkinter as tk
from tkinter import messagebox

class MiniChronometre:
    def __init__(self, root):
        self.root = root
        
        # Supprime les bordures et la barre de titre
        self.root.overrideredirect(True)
        # Garde la fenêtre toujours au premier plan
        self.root.attributes("-topmost", True)
        
        # Variables de temps et d'état
        self.secondes_ecoulees = 0
        self.en_pause = False
        
        # Création de l'affichage
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 20, "bold"), 
                              fg="white", bg="black", padx=10, pady=5)
        self.label.pack()

        # Centrage de la fenêtre au démarrage
        self.root.update_idletasks()
        largeur = self.root.winfo_width()
        hauteur = self.root.winfo_height()
        ecran_largeur = self.root.winfo_screenwidth()
        ecran_hauteur = self.root.winfo_screenheight()
        
        x = (ecran_largeur // 2) - (largeur // 2)
        y = (ecran_hauteur // 2) - (hauteur // 2)
        self.root.geometry(f"+{x}+{y}")

        # Événements pour déplacer la fenêtre avec le clic gauche
        self.label.bind("<Button-1>", self.debut_deplacement)
        self.label.bind("<B1-Motion>", self.en_deplacement)

        # Création du menu contextuel
        self.menu = tk.Menu(self.root, tearoff=0)
        
        # --- NOUVEAU : La solution pragmatique ---
        self.menu.add_command(label="Pause", command=self.basculer_pause)
        self.menu.add_command(label="Définir le temps...", command=self.definir_temps)
        self.menu.add_separator()
        self.menu.add_command(label="Réinitialiser à zéro", command=self.reinitialiser)
        self.menu.add_separator()
        self.menu.add_command(label="Fermer le menu", command=self.fermer_menu)
        self.menu.add_command(label="À propos", command=self.afficher_a_propos)
        self.menu.add_command(label="Quitter", command=self.quitter)

        # Événement pour le clic droit
        self.label.bind("<Button-3>", self.afficher_menu)
        
        # Lancement du chronomètre
        self.mettre_a_jour_temps()

    def debut_deplacement(self, event):
        self.x = event.x
        self.y = event.y
        self.fermer_menu() # Ferme le menu si on déplace le bloc

    def en_deplacement(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def afficher_menu(self, event):
        # Affiche simplement le menu à la position de la souris
        self.menu.post(event.x_root, event.y_root)

    def fermer_menu(self):
        """Masque le menu grâce à l'option dédiée."""
        self.menu.unpost()

    def basculer_pause(self):
        self.en_pause = not self.en_pause
        if self.en_pause:
            self.menu.entryconfig(0, label="Reprendre")
            self.label.config(fg="gray")
        else:
            self.menu.entryconfig(0, label="Pause")
            self.label.config(fg="white")

    def mettre_a_jour_temps(self):
        if not self.en_pause:
            self.actualiser_affichage_immediat()
            self.secondes_ecoulees += 1
            
        # La boucle d'attente continue de tourner même en pause, sans incrémenter le temps
        self.root.after(1000, self.mettre_a_jour_temps)

    def actualiser_affichage_immediat(self):
        heures = self.secondes_ecoulees // 3600
        minutes = (self.secondes_ecoulees % 3600) // 60
        secondes = self.secondes_ecoulees % 60
        self.label.config(text=f"{heures:02d}:{minutes:02d}:{secondes:02d}")

    def reinitialiser(self):
        self.secondes_ecoulees = 0
        self.actualiser_affichage_immediat()

    def calculer_position_decalee(self):
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty() + 60
        return f"+{x}+{y}"

    def definir_temps(self):
        fenetre_temps = tk.Toplevel(self.root)
        fenetre_temps.title("Définir le temps")
        fenetre_temps.geometry(self.calculer_position_decalee())
        fenetre_temps.transient(self.root)
        fenetre_temps.grab_set()

        tk.Label(fenetre_temps, text="Entrez la nouvelle valeur (HH:MM:SS) :").pack(padx=10, pady=(10, 5))
        
        entree = tk.Entry(fenetre_temps)
        entree.pack(padx=10, pady=5)
        entree.focus_set()

        def valider(event=None):
            saisie = entree.get()
            try:
                h, m, s = map(int, saisie.split(':'))
                self.secondes_ecoulees = h * 3600 + m * 60 + s
                self.actualiser_affichage_immediat()
                fenetre_temps.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Format invalide. Utilisez HH:MM:SS.", parent=fenetre_temps)

        tk.Button(fenetre_temps, text="Valider", command=valider).pack(pady=(5, 10))
        fenetre_temps.bind('<Return>', valider)

    def afficher_a_propos(self):
        fenetre_propos = tk.Toplevel(self.root)
        fenetre_propos.title("À propos")
        fenetre_propos.geometry(self.calculer_position_decalee())
        fenetre_propos.transient(self.root)
        fenetre_propos.grab_set()

        texte = "Mini Chronomètre Tkinter\n\nAuteur : Gemini\nDate : 18 Février 2026\nVersion : 1.8"
        tk.Label(fenetre_propos, text=texte, justify="center").pack(padx=20, pady=15)
        tk.Button(fenetre_propos, text="OK", command=fenetre_propos.destroy).pack(pady=(0, 10))

    def quitter(self):
        self.root.destroy()

if __name__ == "__main__":
    racine = tk.Tk()
    app = MiniChronometre(racine)
    racine.mainloop()
