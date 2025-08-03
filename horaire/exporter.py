import os
from datetime import datetime, timedelta
import shutil
import locale
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "C")


class HoraireExporter:
    def __init__(self, output_path="../database/horaire.html", css_path="style.css"):
        self.output_path = output_path
        self.css_path = css_path
        print(f"🔄 Initialisation de l'exportateur avec le chemin : {self.output_path} et le CSS : {self.css_path}")

    def export(self, jours_map, jours_feries, cours_par_jour):
        
        print("🔄 Exportation de l'horaire inside méthod")
        
        if os.path.exists(self.output_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy(self.output_path, f"{self.output_path}.{timestamp}.bak")

        html = [
            "<!DOCTYPE html>",
            "<html lang='fr'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            "    <title>Planning UMONS</title>",
            f"    <link rel='stylesheet' href='{self.css_path}'>",
            "</head>",
            "<body>",
            "  <div class='container'>",
            "    <h1 class='title'>Planning de la semaine</h1>",
            "    <div class='grid'>"
        ]

        for jour in jours_map.values():
            
            output_dir = os.path.dirname(self.output_path)
            filename = f"{jour.replace(' ', '_').lower()}.html"
            
            if jour in jours_feries:
                html.append(
                    f"<a class='card ferie' href='{filename}'>"
                    f"<h2><svg viewBox='0 0 24 24'><path d='M3 8h18M8 3v2m8-2v2M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'/></svg> {jour}</h2>"
                    f"<div class='ferie-content'>"
                    f"<svg viewBox='0 0 24 24'><path d='M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'/></svg>"
                    f"<p>Férié</p><span>Jour de repos</span>"
                    f"</div></a>"
                )
            elif jour in cours_par_jour:
                html.append(f"<a class='card' href='{filename}'><h2><svg viewBox='0 0 24 24'><path d='M3 8h18M8 3v2m8-2v2M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'/></svg> {jour}</h2><div class='courses'>")
                for ligne in sorted(cours_par_jour[jour]):
                    heure, reste = ligne.split(" | ", 1)
                    nom, salles = reste.split(" | Salles : ", 1)
                    html.append(
                        "<div class='course-block'>"
                        f"<div class='heure'><svg viewBox='0 0 24 24'><path d='M12 6v6l4 2'/><circle cx='12' cy='12' r='10'/></svg>{heure}</div>"
                        f"<div class='nom'>{nom}</div>"
                        f"<div class='salle'>{salles}</div>"
                        "</div>"
                    )
                html.append("</div></a>")
            else:
                html.append(
                    f"<a class='card' href='{filename}'>"
                    f"<h2><svg viewBox='0 0 24 24'><path d='M3 8h18M8 3v2m8-2v2M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'/></svg> {jour}</h2>"
                    f"<div class='no-course'>"
                    f"<svg viewBox='0 0 24 24'><path d='M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z'/></svg>"
                    f"<p>Aucun cours</p>"
                    f"</div></a>"
                )

        html += [
            "    </div>",
            f"    <div class='footer'>Semaine du {self._get_date_range()}</div>",
            "  </div>",
            "</body>",
            "</html>"
        ]
        
        print(f"HTML généré, écriture dans le fichier {self.output_path}")
        

        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
            
        print(f"✅ Fichier généré : {self.output_path}")


        # Générer une page détaillée pour chaque jour
        
        output_dir = os.path.dirname(self.output_path)
        for jour in jours_map.values():
            filename = os.path.join(output_dir, f"{jour.replace(' ', '_').lower()}.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self._build_day_page(jour, cours_par_jour.get(jour, []), jour in jours_feries))
            print(f"✅ Fichier détaillé généré : {filename}")
            
            
    def _build_day_page(self, jour, cours, ferie=False):
        html = [
            "<!DOCTYPE html>",
            "<html lang='fr'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"  <link rel='stylesheet' href='{self.css_path}'>",
            "  <title>Détail du jour</title>",
            "</head>",
            "<body>",
            "  <div class='container'>",
            f"    <h1 class='title'>{jour}</h1>",
        ]

        if ferie:
            html += [
                "<div class='card ferie' style='text-align:center'>",
                "<div class='ferie-content'>",
                "<svg viewBox='0 0 24 24'><path d='M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'/></svg>",
                "<p>Férié</p><span>Jour de repos</span>",
                "</div></div>"
            ]
        elif not cours:
            html += [
                "<div class='card' style='text-align:center'>",
                "<div class='no-course'>",
                "<svg viewBox='0 0 24 24'><path d='M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z'/></svg>",
                "<p>Aucun cours</p>",
                "</div></div>"
            ]
        else:
            html += ["<div class='card'><div class='courses'>"]
            for ligne in sorted(cours):
                heure, reste = ligne.split(" | ", 1)
                nom, salles = reste.split(" | Salles : ", 1)
                html.append(
                    "<div class='course-block'>"
                    f"<div class='heure'><svg viewBox='0 0 24 24'><path d='M12 6v6l4 2'/><circle cx='12' cy='12' r='10'/></svg>{heure}</div>"
                    f"<div class='nom'>{nom}</div>"
                    f"<div class='salle'><svg viewBox='0 0 24 24'><path d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/></svg> {salles}</div>"
                    "</div>"
                )
            html += ["</div></div>"]

        html += [
            "<div style='text-align:center;margin-top:1.5rem;'>",
            "<a href='horaire.html' class='btn-retour'>Retour à la semaine</a>",
            "</div>",
            "</div>",
            "</body>",
            "</html>"
        ]
        return "\n".join(html)
    
    def _get_date_range(self):
        today = datetime.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=4)

        mois_fr = {
            "January": "janvier", "February": "février", "March": "mars", "April": "avril",
            "May": "mai", "June": "juin", "July": "juillet", "August": "août",
            "September": "septembre", "October": "octobre", "November": "novembre", "December": "décembre",
            "janvier": "janvier", "février": "février", "mars": "mars", "avril": "avril",
            "mai": "mai", "juin": "juin", "juillet": "juillet", "août": "août",
            "septembre": "septembre", "octobre": "octobre", "novembre": "novembre", "décembre": "décembre"
        }

        mois_debut_en = start.strftime("%B")
        mois_fin_en = end.strftime("%B")

        mois_debut = mois_fr.get(mois_debut_en, mois_debut_en)
        mois_fin = mois_fr.get(mois_fin_en, mois_fin_en)

        if mois_debut == mois_fin:
            return f"{start.day} au {end.day} {mois_fin} {start.year}"
        else:
            return f"{start.day} {mois_debut} au {end.day} {mois_fin} {start.year}"


