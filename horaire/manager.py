# scraper.py (à la suite de HoraireScraper)

import os
from scraper import HoraireScraper
from exporter import HoraireExporter


class HoraireManager:
    def __init__(self):
        print("🔄 Initialisation du gestionnaire d'horaire...")
        self.scraper = HoraireScraper(
            target_label=".Bloc compl. MA - Sc. informatiques"
        )


    def run(self):
        print("🔄 Démarrage du gestionnaire d'horaire...")
        try:
            print("🔄 Mise à jour de l'horaire en cours manager...")
            jours_map, jours_feries, cours_par_jour = self.scraper.recuperer_horaire()
            exporter = HoraireExporter()
            exporter.export(jours_map, jours_feries, cours_par_jour)
            print("✅ Horaire mis à jour.")
        except Exception as e:
            print("⚠️ Échec de récupération :", e)
            if os.path.exists("horaire.html"):
                print("➡️ Utilisation du dernier horaire sauvegardé.")
            else:
                print("❌ Aucune sauvegarde disponible.")
        finally:
            self.scraper.close()
