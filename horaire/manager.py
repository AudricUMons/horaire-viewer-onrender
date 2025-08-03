import os
from scraper import HoraireScraper
from exporter import HoraireExporter


class HoraireManager:
    def __init__(self):
        self.scraper = HoraireScraper(
            target_label=".Bloc compl. MA - Sc. informatiques"
        )

    def run(self):
        try:
            database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
            os.makedirs(database_path, exist_ok=True)

            jours_map, jours_feries, cours_par_jour = self.scraper.recuperer_horaire()

            output_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "database",
                "horaire.html"
            )
            exporter = HoraireExporter(output_path=output_path, css_path="style.css")
            exporter.export(jours_map, jours_feries, cours_par_jour)
        except Exception as e:
            backup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "horaire.html")
            if os.path.exists(backup_path):
                print("➡️ Utilisation du dernier horaire sauvegardé.")
            else:
                print("❌ Aucune sauvegarde disponible.")
        finally:
            self.scraper.close()
