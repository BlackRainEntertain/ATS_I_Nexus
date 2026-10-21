@echo off
chcp 65001 >nul
title NEXUS_STREAM_SPLITTER_v1.2
color 0b

echo =======================================================================
echo [!] ATS_I Nexus - Central History Splitter Engine (v1.2 - Clean Engine)
echo =======================================================================
echo.
echo Dieses Skript zerlegt die gefundene Textdatei vollautomatisch
echo in perfekt portionierte User-Message-Chunks für Google AI.
echo.
timeout /t 1 >nul

:: Temporäre Python-Datei direkt erzeugen
(
echo import os
echo base_dir = os.getcwd^(^)
echo txt_path = ""
echo for f in os.listdir^(base_dir^):
echo     if f.endswith^(".txt"^) and "migration" not in f.lower^(^):
echo         txt_path = os.path.join^(base_dir, f^); break
echo if not txt_path: print^("[ERROR] Keine passende .txt-Datei gefunden!"^); exit^(^)
echo print^(f"[i] Gefundene Quelldatei: {os.path.basename(txt_path)}"^)
echo with open^(txt_path, "r", encoding="utf-8", errors="ignore"^) as f: text = f.read^(^)
echo limit = 7450
echo chunks = [text[i:i+limit] for i in range^(0, len^(text^), limit^)]
echo out_file = os.path.join^(base_dir, "NEXUS_MIGRATION_STREAM.txt"^)
echo with open^(out_file, "w", encoding="utf-8"^) as f:
echo     for idx, chunk in enumerate^(chunks^):
echo         f.write^(f"\n║ [NEXUS_STREAM: CHUNK {idx+1}/{len(chunks)}]\n"^)
echo         f.write^(chunk.strip^(^) + "\n║\n"^)
echo print^(f"[SUCCESS] Stream-Datei erzeugt: {len(chunks)} Pakete bereit in NEXUS_MIGRATION_STREAM.txt!"^)
) > split_history.py

py split_history.py
if exist split_history.py del /f /q split_history.py

echo.
echo =======================================================================
echo [DONE] Datenblöcke erfolgreich aufbereitet!
echo Du kannst das Layout jetzt in aller Ruhe vorbereiten.
echo =======================================================================
timeout /t 3 >nul
exit


