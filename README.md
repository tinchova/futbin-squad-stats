# 🟦 Futbin Scraper - FIFA 25 Squad Stats

Script en Python para scrapear estadísticas de jugadores de Futbin, procesarlas y exportarlas automáticamente a Google Sheets.

---

## ✅ Requisitos

### 1. Python

Descargá e instalá la última versión de Python desde:  
👉 https://www.python.org/downloads/

⚠️ Durante la instalación, asegurate de marcar `✔ Add Python to PATH`.

### 2. Google Chrome + ChromeDriver

1. Verificá tu versión de Chrome (`chrome://settings/help`)
2. Descargá el ChromeDriver correspondiente:  
   👉 https://chromedriver.chromium.org/downloads
3. Extraelo en una carpeta fija, por ejemplo:

```plaintext
C:/webdrivers/chromedriver.exe
```

---

## ⚙️ Instalación del proyecto

### Cloná el repositorio

```bash
git clone https://github.com/tu-usuario/futbin-squad-stats.git
cd futbin-squad-stats
```

### Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
.env\Scriptsctivate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📄 requirements.txt

```txt
selenium
pandas
gspread
oauth2client
```

---

## 📁 Archivos necesarios

- `futbin_scraper.py`: Script principal
- `credenciales.json`: Archivo de Google Service Account

Colocá `credenciales.json` en el directorio del proyecto.

---

## 🔐 Configuración de Google Sheets

1. Creá un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitá la API de Google Sheets
3. Creá una cuenta de servicio y descargá el `.json`
4. Compartí tu Google Sheet con el `client_email` de ese `.json` como **editor**
5. Asegurate de que tu planilla tenga:
   - Una hoja llamada `URLS` con los links a los jugadores
   - Una hoja llamada `Jugadores` (el script escribirá allí los datos)

---

## ▶️ Ejecución

```bash
python futbin_scraper.py
```

El script leerá las URLs desde la hoja `URLS`, procesará cada jugador, y escribirá los datos en la hoja `Jugadores` dentro de la misma planilla de Google Sheets.

---

## ✅ Output

Los datos extraídos incluyen:

- Nombre, valoración, posición, posiciones secundarias
- Playstyles (con y sin "+")
- Stats globales (Pace, Shooting, etc.)
- Substats detalladas (Dribbling, Short Pass, Strength, etc.)

---

## 📌 Licencia

Este proyecto es de uso personal y educativo.
