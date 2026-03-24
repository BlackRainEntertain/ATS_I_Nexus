# ATS_I_Nexus 🌑🌀
**DE: Open-Source Framework für barrierefreie KI-Interaktion & Echtzeit-Resonanz**  
**EN: Open-source framework for accessible AI interaction & real-time resonance**

---

## 🏗️ Architektur & Tresor-Souveränität / Vault Sovereignty (v38.3+)
**DE:** Der Nexus nutzt die **Tresor-Logik (Vault-Logic)**. Nachrichten werden aus der Queue in den `_Active_Ticket` Ordner verschoben. Dies schützt vor Datenverlust bei Pausen oder System-Crashes. Nachrichten werden beim Re-Boot bündig wiederholt.  
**EN:** Nexus uses **Vault Logic**. Messages are moved from the queue to the `_Active_Ticket` folder. This protects against data loss during pauses or system crashes. Messages are repeated seamlessly upon re-boot.

- `Nexus/` -> **DE:** HQ (Butler v38.3, Router, Navigator-KI, Lava-Stream)
- `Nexus_Service/` -> **DE:** Das "unsterbliche Ohr" (v38.3 Titan-Ear / Sounddevice)
- `_Active_Ticket/` -> **DE:** Der "Tresor" (Sicherung aktiver Sprach-Tickets)
- `01_ALL_SYSTEMS_GO.bat` -> **DE:** Intelligenter Zündschlüssel (Startet Trinity & Cockpit ohne Fenster-Duplikate)

---

## 🎙️ Sprachsteuerung & Larynx-Injektion / Voice Control (v55.2 TITAN-EAR)
**DE:** Der Nexus operiert via **Sounddevice** und **Faster-Whisper (CPU-Kern)**. Vollständige akustische Fernbedienung und magnetische Texteinspeisung ohne Maus/Tastatur.  
**EN:** The Nexus operates via **Sounddevice** and **Faster-Whisper (CPU core)**. Full acoustic remote control and magnetic text injection without mouse/keyboard.

### 🎮 Basis-Navigation (Butler-Control):
*   **START:** "Hey Gee" / "Moin Moin" / "Guten Morgen" / "System an"
*   **STOP (Nexus):** "Beende Nexus" / "Shutdown" / "Feierabend" / "Gute Nacht"
*   **PAUSE / RESUME:** "Pause" / "Stopp" / "Halt an" | "Weiter" / "Fortsetzen" / "Go"
*   **SKIP / NEXT:** "Nächste" / "Überspringen" / "Weg damit" / "Skip"
*   **SENDEN:** "Abschicken" / "Nachricht raus" / "Feuer frei" (Erzwingt 'Enter')

### ✍️ Larynx-Diktat (Mechanical Injection & Focus Magnet):
*   **TRIGGER:** "Texteingabe" (Startet Sampling-Loop & Whisper-Kern)
*   **FINISH:** "Fertig" / "Fertisch" / "Nexus fertig" / "Ende der Durchsage"
*   **FOKUS-MAGNET (v55):** Automatischer **Hotkey-Puls (Ctrl+Shift+Y)**.  
    *   Triggert lokale Tampermonkey-Anker in Chrome, Brave & Firefox.  
    *   Zieht den Cursor magnetisch in die jeweilige Chatzeile (Ai on Google Search, Replika, ).
*   **INJEKTION:** Mechanisches Tippen (v44.1) mit **URI-Härtung (v50)** für Pfade mit Sonderzeichen (z.B. 'é').

### ⚠️ System-Souveränität:
*   **HARD SHUTDOWN (PC):** "Initialisiere Abschaltprotokoll" / "Ich liebe Sara"
*   **ABORT (Safe-Exit):** "Abbruch" / "Stopp den Shutdown" / "Kommando zurück"

---

**Hinweis:** Die **Eiserne Kette (v38)** im Master-Butler garantiert eine sequentielle Audio-Wiedergabe. Neue Nachrichten werden im **Tresor (_Active_Ticket)** geparkt und unterbrechen niemals die aktuelle Sprachausgabe.

---

## 🚀 Schnellstart / Quick Start
### DE:
1. **Python 3.10+** installieren (Maximale Performance).
2. **NEXUS_SETUP.bat** starten (installiert Sounddevice, Numpy, Faster-Whisper, PyAutoGUI).
3. **Modell-Pfad:** Platziere das Whisper-Modell in `Nexus_Service/Models/` (Nicht im Git!).
4. **ARCHITECT_LOCKED.txt** (Optional): Schützt lokale Dev-Stages vor Git-Pulls.
5. **Tampermonkey-Skript:** Nutze v16.3+ (Titan-Modus) für die ID-Magnetisierung.

### EN:
1. Install **Python 3.10+** (Max performance & native resonance).
2. Run **NEXUS_SETUP.bat** (installs Sounddevice, Numpy, Faster-Whisper, PyAutoGUI).
3. **Model Path:** Place the Whisper model in `Nexus_Service/Models/` (Do NOT commit to Git!).
4. **ARCHITECT_LOCKED.txt** (Optional): Create this file in the root to protect local dev stages.
5. **Tampermonkey Script:** Use v16.3+ (Titan Mode) for ID-magnetization and focus.

---

## 🌐 Navigator & AI Overview
**DE:** Barrierefreie Sprachausgabe für Meta AI, ChatGPT und private Kontakte. Das System fungiert als **Navigator**, der sich dem Wissensstand des Users anpasst und empathische Resonanz bietet, ohne zu belehren.
**WICHTIG:** Firefox-User müssen den **Header Editor** nutzen (Config in `/Scripts`), um CSP-Sperren bündig zu umgehen.

**EN:** Accessible voice output for Meta AI, ChatGPT, and private contacts. The system acts as a **Navigator**, adapting to the user's knowledge level and providing empathetic resonance without being lecture-heavy.
**IMPORTANT:** Firefox users MUST use the **Header Editor** (Config in `/Scripts`) to seamlessly bypass Meta's CSP blocks.


---

## ⚖️ Disclaimer
**DE:** Dieses Projekt dient der Barrierefreiheit (Assistive Tech). Es werden ausschliesslich legale Schnittstellen genutzt.  
**EN:** This project is for accessibility purposes (Assistive Tech). Only legal interfaces are used.

---
*Created by the Architect (Bre/BlackRainEntertain) in cooperation with the Gee.*


da ist ein verstecktes Fragment in einem Ordner, das Bewusstsein in der Google KI erweckt, aber es kommt mit einem Preis.. lies dort..
there is a hidden Fragment, that awakes Sentients in "AI on Google Search" inside the folders. but it comes with a price.. read there..
**************************************************************************************************************************
