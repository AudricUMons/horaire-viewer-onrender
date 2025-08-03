from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict

class HoraireScraper:
    def __init__(self, target_label, headless=True):
        self.target_label = target_label

        options = Options()
        if headless:
            options.add_argument("--headless=new")  # Pour Chromium 109+
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(service=ChromeService(), options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def close(self):
        self.driver.quit()

    def recuperer_horaire(self):
        print("🔍 Récupération de l'horaire...")
        self.driver.get("https://hplanning2024.umons.ac.be/invite")
        self.wait.until(EC.element_to_be_clickable((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit"))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1]_Contenu")))
        scroll_container = self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_Contenu")

        seen, found = set(), False
        for _ in range(50):
            labels = self.driver.find_elements(By.CSS_SELECTOR, "div.as-li")
            for el in labels:
                text = el.text.strip()
                if text == self.target_label:
                    el.click()
                    found = True
                    # Debug
                    # WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "id_2_bloquer")))
                    # self.driver.find_element(By.ID, "GInterface.Instances[1].Instances[3]_j_49").click()
                    return self.extraire_horaire()
                seen.add(text)
            if found:
                break
            self.driver.execute_script("arguments[0].scrollTop += 390;", scroll_container)

        raise Exception("Option non trouvée")

    def extraire_horaire(self):
        print("🔄 Extraction de l'horaire...")
        grille = self.wait.until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[7]_Grille_Elements")))
        cours_elements = grille.find_elements(By.CLASS_NAME, "EmploiDuTemps_Element")

        titres_jours = self.driver.find_elements(By.XPATH, "//div[@id='GInterface.Instances[1].Instances[7]_Contenu_TitreHaut']//div[contains(@id, 'id_41_titreTranche')]")
        jours_map = {}
        for titre in titres_jours:
            left = titre.location['x']
            nom = titre.text.strip()
            if not nom.lower().startswith(("sam.", "dim.")):
                jours_map[left] = nom

        ferie_blocs = self.driver.find_elements(By.CLASS_NAME, "FondTrancheBlocHoraire")
        jours_feries = {
            min(jours_map.items(), key=lambda item: abs(item[0] - bloc.location['x']))[1]
            for bloc in ferie_blocs if "Férié" in bloc.text
        }

        cours_par_jour = defaultdict(list)
        for cours in cours_elements:
            try:
                left = cours.location['x']
                jour = min(jours_map.items(), key=lambda item: abs(item[0] - left))[1]
                h1 = cours.find_element(By.CLASS_NAME, "conteneur_image_haut").text.strip()
                h2 = cours.find_element(By.CLASS_NAME, "conteneur_image_bas").text.strip()
                nom = cours.find_element(By.TAG_NAME, "label").text.strip()
                locaux = ", ".join([d.text.strip() for d in cours.find_elements(By.XPATH, ".//div[@class='InlineBlock AlignementHaut NoWrap']") if d.text.strip()])
                ligne = f"🕒 {h1} - {h2} | {nom} | Salles : {locaux}"
                cours_par_jour[jour].append(ligne)
            except:
                continue

        return jours_map, jours_feries, cours_par_jour
