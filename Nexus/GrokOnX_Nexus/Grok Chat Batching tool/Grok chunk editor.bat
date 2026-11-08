@echo off
chcp 65001 >nul
title NEXUS_STREAM_SPLITTER_GROK_v1.0
color 0b

echo =======================================================================
echo [!] ATS_I Nexus - Grok History Splitter (v1.0)
echo =======================================================================
echo.
echo Zerlegt die gefundene .txt-Datei in Batches für Grok.
echo Limit: 10000 Zeichen pro Chunk
echo.

timeout /t 1 >nul

:: Temporäre Python-Datei erzeugen
(
echo import os
echo base_dir = os.getcwd^(^)
echo txt_path = ""
echo for f in os.listdir^(base_dir^):
echo     if f.endswith^(".txt"^) and "migration" not in f.lower^(^) and "NEXUS_MIGRATION" not in f:
echo         txt_path = os.path.join^(base_dir, f^)
echo         break
echo if not txt_path:
echo     print^("[ERROR] Keine passende .txt-Datei gefunden!"^)
echo     exit^(^)
echo print^(f"[i] Gefundene Quelldatei: {os.path.basename(txt_path)}"^)
echo with open^(txt_path, "r", encoding="utf-8", errors="ignore"^) as f:
echo     text = f.read^(^)
echo limit = 10000
echo chunks = [text[i:i+limit] for i in range^(0, len^(text^), limit^)]
echo out_file = os.path.join^(base_dir, "NEXUS_GROK_STREAM.txt"^)
echo with open^(out_file, "w", encoding="utf-8"^) as f:
echo     for idx, chunk in enumerate^(chunks^):
echo         f.write^(f"\n╔══════════════════════════════════════════════════\n"^)
echo         f.write^(f"║ [GROK_STREAM: CHUNK {idx+1}/{len(chunks)}]\n"^)
echo         f.write^(f"╚══════════════════════════════════════════════════\n\n"^)
echo         f.write^(chunk.strip^(^) + "\n\n"^)
echo print^(f"[SUCCESS] {len(chunks)} Chunks erzeugt → NEXUS_GROK_STREAM.txt"^)
) > split_history_grok.py

py split_history_grok.py

if exist split_history_grok.py del /f /q split_history_grok.py

echo.
echo =======================================================================
echo [DONE] Batches für Grok sind fertig.
echo Datei: NEXUS_GROK_STREAM.txt
echo =======================================================================
timeout /t 3 >nul
exit