import csv
import pandas as pd
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials


# ============================
# CONFIGURACIÓN
# ============================


# Ruta del archivo de credenciales JSON
credenciales_path = ""


# URL de la planilla de Google Sheets
spreadsheet_url = ""


# Nombre de la hoja con las URLs
sheet_urls_name = "URLS"


# Nombre de la hoja donde se escriben los datos
sheet_output_name = "Jugadores"


# ============================
# AUTENTICACIÓN GOOGLE SHEETS
# ============================


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciales = ServiceAccountCredentials.from_json_keyfile_name(credenciales_path, scope)
cliente = gspread.authorize(credenciales)
spreadsheet = cliente.open_by_url(spreadsheet_url)


# Leer URLs de la hoja "URLS"
sheet_urls = spreadsheet.worksheet(sheet_urls_name)
urls = [cell for cell in sheet_urls.col_values(1) if cell.startswith("http")]
print(f"🔗 {len(urls)} URLs encontradas en hoja '{sheet_urls_name}'")


# ============================
# SELENIUM SETUP
# ============================


options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


driver = webdriver.Chrome(
    service=Service("C:/webdrivers/chromedriver.exe"),
    options=options
)


# ============================
# FUNCIONES DE SCRAPING
# ============================


def safe_find_text(by, selector, default=""):
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, selector))
        ).text.strip()
    except:
        return default


todos_los_jugadores = []
campos_substats_unicos = set()


for url in urls:
    print(f"\n🟦 Procesando: {url}")
    driver.get(url)


    jugador = {}


    jugador["Nombre"] = safe_find_text(By.CLASS_NAME, "playercard-25-name")
    jugador["Valoración"] = safe_find_text(By.CLASS_NAME, "playercard-25-rating")
    pos_principal = safe_find_text(By.CLASS_NAME, "playercard-25-position")
    plus = safe_find_text(By.CLASS_NAME, "playercard-25-role-plus")
    jugador["Posición principal"] = pos_principal + plus


    # Posiciones secundarias
    pos_alternativas = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table.narrow-table tr")
    for row in rows:
        try:
            label = row.find_element(By.TAG_NAME, "th").text.strip()
            if label == "Alt POS":
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                if value:
                    pos_alternativas = [p.strip() for p in value.split(",")]
                break
        except:
            continue
    jugador["Posiciones secundarias"] = ", ".join(pos_alternativas)


    # Playstyles
    playstyle_elements = driver.find_elements(By.CSS_SELECTOR, ".playStyle-table-icon")
    playstyles = []
    for el in playstyle_elements:
        try:
            ps_name = el.find_element(By.CLASS_NAME, "slim-font").text.strip()
            is_plus = "psplus" in el.get_attribute("class")
            playstyles.append(ps_name + ("+" if is_plus else ""))
        except:
            continue
    jugador["Playstyles"] = ", ".join(playstyles)


    # Stats principales + substats
    all_stats = {}
    stat_blocks = driver.find_elements(By.CSS_SELECTOR, ".player-stat-wrapper[data-base-stat-id]")
    for block in stat_blocks:
        try:
            base_name = block.find_element(By.CLASS_NAME, "player-stat-name").text.strip()
            base_value = int(block.find_element(By.CLASS_NAME, "player-stat-value").get_attribute("data-stat-value"))
            all_stats[base_name] = base_value
            campos_substats_unicos.add(base_name)
        except:
            pass


        try:
            substats = block.find_elements(By.CSS_SELECTOR, ".column .player-stat-row")
            for row in substats:
                name = row.find_element(By.CLASS_NAME, "player-stat-name").text.strip()
                value = row.find_element(By.CLASS_NAME, "player-stat-value").get_attribute("data-stat-value")
                if name and value:
                    all_stats[name] = int(value)
                    campos_substats_unicos.add(name)
        except:
            continue


    for stat_name in all_stats:
        jugador[stat_name] = all_stats[stat_name]


    todos_los_jugadores.append(jugador)


driver.quit()


# ============================
# EXPORTAR A GOOGLE SHEETS
# ============================


df = pd.DataFrame(todos_los_jugadores)


# Asegurar que todas las columnas estén presentes
columnas_fijas = ["Nombre", "Valoración", "Posición principal", "Posiciones secundarias", "Playstyles"]
todas_las_columnas = columnas_fijas + sorted(campos_substats_unicos)
df = df.reindex(columns=todas_las_columnas)


# Escribir en la hoja "Jugadores"
sheet_output = spreadsheet.worksheet(sheet_output_name)
sheet_output.clear()
sheet_output.update([df.columns.values.tolist()] + df.fillna("").values.tolist())


print(f"\n✅ {len(df)} jugadores exportados a la hoja '{sheet_output_name}'")



