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
            print('Vérification de l\'existence du dossier de base de données...')
            database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
            os.makedirs(database_path, exist_ok=True)
            print("🔄 Mise à jour de l'horaire en cours manager...")
            jours_map, jours_feries, cours_par_jour = self.scraper.recuperer_horaire()
            print("✅ Horaire récupéré avec succès.")
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "database",
                "horaire.html"
            )
            exporter = HoraireExporter(output_path=output_path, css_path="style.css")
            print("🔄 Exportation de l'horaire...")
            exporter.export(jours_map, jours_feries, cours_par_jour)
            print("✅ Horaire mis à jour.")
        except Exception as e:
            print("⚠️ Échec de récupération :", e)
            backup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "horaire.html")
            if os.path.exists(backup_path):
                print("➡️ Utilisation du dernier horaire sauvegardé.")
            else:
                print("❌ Aucune sauvegarde disponible.")
        finally:
            self.scraper.close()
