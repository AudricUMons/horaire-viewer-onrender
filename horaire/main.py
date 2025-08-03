# main.py

from manager import HoraireManager
import os


def afficher_arborescence(base_path, prefix=""):
    try:
        for nom in os.listdir(base_path):
            chemin = os.path.join(base_path, nom)
            if os.path.isdir(chemin):
                print(f"{prefix}📁 {nom}/")
                afficher_arborescence(chemin, prefix + "  ")
            else:
                print(f"{prefix}📄 {nom}")
    except Exception as e:
        print(f"{prefix}❌ Impossible d'accéder à {base_path} : {e}")



if __name__ == "__main__":
    print("🔄 Mise à jour de l'horaire en cours...")
    print("\n📂 Arborescence autour du script :")
    racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    afficher_arborescence(racine)
    HoraireManager().run()

