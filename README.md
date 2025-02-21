## English

### Overview
This Discord bot allows moderators to grant temporary VIP rights to players via Discord. The bot uses:
- A Python script (`bot.py`)
- Environment variables (for configuration)
- A `language.json` for multilingual support
- An API client (`api_client.py`) that communicates with your backend
- The Discord Python API (`discord.py`)

### Features
- **Button-based workflow** in a specific channel, allowing easy VIP assignment  
- **Modal input** for entering player name/ID  
- **Automatic search** in your backend (via API) to fetch player details  
- **Direct Message (DM)** to the moderator to confirm data and finalize VIP  
- **Multilingual** support (e.g., English, German) using `language.json`  
- **Logging** of successful VIP grants in a specified channel  

---

### Prerequisites
- Python 3.8+
- A [Discord application](https://discord.com/developers/applications) with a bot token
- `discord.py` library (v2.x)
- A working API endpoint for fetching and updating player data

---

### Installation

1. **Clone the repository** or copy the files (`bot.py`, `api_client.py`, `language.json`, etc.) into your project.
2. **Create** (or update) a file named `.env` in the same folder as `bot.py`. Example:
   ```bash
   DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
   API_BASE_URL=https://your-api.example.com
   API_TOKEN=YOUR_API_AUTH_TOKEN
   ALLOWED_CHANNEL_ID=123456789012345678
   VIP_LOG_CHANNEL_ID=123456789012345679
   LANG_CODE=en
   ```
3. **Install dependencies** (e.g., using pip):
   ```bash
   pip install -r requirements.txt
   ```
   Make sure `discord.py`, `python-dotenv`, etc. are listed in `requirements.txt`.

4. **Configure** your `language.json` with the relevant translations (e.g., English, German). Ensure you have matching keys for all used texts.

---

### Usage

1. **Start the bot** by running:
   ```bash
   python bot.py
   ```
   The bot will go online and print:
   ```
   Bot <BotName> is online. ID=<IDNumber>
   ```
2. **Check the designated Discord channel** (ID specified by `ALLOWED_CHANNEL_ID`). The bot posts (or updates) a message with a button labeled something like “Grant 2 hours of VIP”.  
3. **As a moderator**, click on that button to open the modal for entering the player’s name or ID.  
4. **Submit** the modal. The bot fetches data from the API and sends you a **DM** with the player details.  
5. **In the DM**, you can:
   - **Grant VIP** (green button)  
   - **Cancel** (red button)  
6. If you choose **Grant VIP**, the bot will:
   - Call the API to assign VIP
   - Log the action in the channel specified by `VIP_LOG_CHANNEL_ID`

---

### Environment Variables
| Variable             | Description                                           | Example                      |
|----------------------|-------------------------------------------------------|------------------------------|
| DISCORD_BOT_TOKEN    | Your bot token from the Discord Developer Portal      | `OTMzOT...`                  |
| API_BASE_URL         | Base URL for your API                                 | `https://api.example.com`    |
| API_TOKEN            | Token or key to authorize requests to your API        | `3c314d88-89ba-4c27-a1d5-f754569660cf`                  |
| ALLOWED_CHANNEL_ID   | The Discord channel ID where the “Grant VIP” button is posted | `123456789012345678` |
| VIP_LOG_CHANNEL_ID   | The Discord channel ID where each VIP grant is logged | `234567890123456789`         |
| LANG_CODE            | Language code used for loading text from `language.json`  | `en` or `de`                |

**Note**: Make sure these values are all set in your `.env` file or in your environment variables.

---

### Extending / Customizing
- **Multilingual support**: Edit or add languages in `language.json`. Ensure the same keys exist for each language.  
- **API calls**: Adjust `api_client.py` to match your real endpoints/method names.  
- **VIP logic**: If you want to grant a different length of VIP time or have additional checks, edit the relevant methods in `ConfirmVIPView`.

---

### Troubleshooting
- **Bot not responding**? Double-check your token, channel IDs, and API endpoints. Check logs in your console.  
- **No data found**? Confirm your API endpoint is correct and the player name/ID is correct.  
- **Language fallback**? If you set `LANG_CODE` to a non-existent key, it automatically defaults to English.

---

### License
(Decide on a license for your project, e.g., MIT, Apache, GPL, etc.)

---

## Deutsch

### Überblick
Dieses Discord-Bot-Skript ermöglicht es Moderatoren, Spielern direkt per Discord VIP-Rechte zu vergeben. Der Bot nutzt:
- Ein Python-Skript (`bot.py`)
- Umgebungsvariablen (zur Konfiguration)
- Eine `language.json` für Mehrsprachigkeit
- Einen API-Client (`api_client.py`), der mit eurer Backend-API kommuniziert
- Die Discord-Python-Bibliothek (`discord.py`)

### Funktionen
- **Button-basierter Workflow** in einem bestimmten Discord-Kanal zur einfachen VIP-Vergabe  
- **Modal-Eingabe** für Spielername/ID  
- **Automatische Suche** per API (zum Abruf der Spielerdaten)  
- **Direktnachricht (DM) an den Moderator**, um Daten zu bestätigen und VIP letztendlich zu vergeben  
- **Mehrsprachig** (z. B. Englisch, Deutsch) via `language.json`  
- **Protokollierung** im angegebenen Kanal, sobald VIP erfolgreich vergeben wurde  

---

### Voraussetzungen
- Python 3.8+
- Eine [Discord-Anwendung](https://discord.com/developers/applications) mit Bot-Token
- `discord.py` (v2.x)
- Eine funktionierende API-Schnittstelle zum Suchen und Ändern von Spielerdaten

---

### Installation

1. **Repository klonen** oder die Dateien (`bot.py`, `api_client.py`, `language.json` etc.) in dein Projekt kopieren.
2. **Erstelle** (oder aktualisiere) eine `.env`-Datei im selben Ordner wie `bot.py`. Beispiel:
   ```bash
   DISCORD_BOT_TOKEN=DEIN_DISCORD_BOT_TOKEN
   API_BASE_URL=https://deine-api.example.com
   API_TOKEN=DEIN_API_AUTH_TOKEN
   ALLOWED_CHANNEL_ID=123456789012345678
   VIP_LOG_CHANNEL_ID=123456789012345679
   LANG_CODE=de
   ```
3. **Installiere Abhängigkeiten** (z. B. via pip):
   ```bash
   pip install -r requirements.txt
   ```
   Achte darauf, dass `discord.py`, `python-dotenv` usw. in der `requirements.txt` aufgeführt sind.

4. **Konfiguriere** deine `language.json` mit den benötigten Übersetzungen (z. B. Englisch, Deutsch). Achte darauf, dass alle im Code verwendeten Keys in jeder Sprache vorhanden sind.

---

### Verwendung

1. **Starte den Bot**:
   ```bash
   python bot.py
   ```
   Der Bot meldet sich mit etwas wie:
   ```
   Bot <BotName> ist online. ID=<IDNummer>
   ```
2. **Prüfe den zugewiesenen Discord-Kanal** (definiert durch `ALLOWED_CHANNEL_ID`). Der Bot postet oder aktualisiert dort eine Nachricht mit einem Button (z. B. „VIP vergeben“).  
3. **Als Moderator** klickst du auf diesen Button, um das Modal zu öffnen, in welchem du den Spielernamen oder die Spieler-ID eingibst.  
4. **Abschicken** des Modals. Der Bot sucht nun nach den Daten in der API und sendet dir eine **DM** mit den gefundenen Informationen.  
5. **In der DM** stehen dir zwei Buttons zur Verfügung:
   - **VIP jetzt vergeben** (grüner Button)  
   - **Vorgang abbrechen** (roter Button)  
6. Wenn du **VIP jetzt vergeben** klickst, wird:
   - Per API VIP an den Spieler vergeben  
   - Ein Embed im Log-Kanal (definiert durch `VIP_LOG_CHANNEL_ID`) gepostet  
   - Beide Buttons werden deaktiviert

---

### Umgebungsvariablen
| Variable             | Beschreibung                                                        | Beispiel                       |
|----------------------|---------------------------------------------------------------------|--------------------------------|
| DISCORD_BOT_TOKEN    | Bot-Token aus dem Discord Developer Portal                          | `OTMzOT...`                    |
| API_BASE_URL         | Basis-URL für eure API                                              | `https://api.beispiel.de`      |
| API_TOKEN            | Token oder Key zur Autorisierung der API-Aufrufe                    | `3c314d88-89ba-4c27-a1d5-f754569660cf`                    |
| ALLOWED_CHANNEL_ID   | Discord-Kanal-ID, in dem der „VIP vergeben“-Button angezeigt wird    | `123456789012345678`           |
| VIP_LOG_CHANNEL_ID   | Discord-Kanal-ID, in dem jede VIP-Vergabe protokolliert wird         | `234567890123456789`           |
| LANG_CODE            | Sprachcode, um die Texte aus `language.json` zu laden               | `en` oder `de`                 |

**Hinweis**: Diese Werte sollten alle in deiner `.env`-Datei (oder Systemumgebung) gesetzt werden.

---

### Erweiterung / Anpassung
- **Mehrsprachigkeit**: Passe die `language.json` an oder füge neue Sprachen hinzu. Jede Sprache braucht dieselben Keys.  
- **API-Aufrufe**: Passe `api_client.py` an die echten Endpunkte eurer API an.  
- **VIP-Logik**: Wenn du eine andere VIP-Dauer oder weitere Prüfungen willst, bearbeite die Methoden in `ConfirmVIPView`.

---

### Fehlerbehebung
- **Bot reagiert nicht**? Überprüfe Token, Kanal-IDs und API-Endpunkte. Sieh in der Konsole nach Logs.  
- **Keine Daten gefunden**? Prüfe, ob dein Suchbegriff korrekt ist und die API korrekt erreichbar ist.  
- **Fallback auf Englisch**? Wenn du `LANG_CODE` auf eine unbekannte Sprache setzt, wechselt das Skript automatisch zu Englisch.

---

### Lizenz
MIT
