@echo off
title --- NEXUS_ALL_SYSTEMS_GO_v6 ---
color 0b

echo [!] Räume alte Frequenzen auf (PowerShell & Python)...
taskkill /f /im powershell.exe /t >nul 2>&1
taskkill /f /im python.exe /t >nul 2>&1

echo [!] Bereinige Nexus-Zentrum (_Voice_Queue)...
if exist "Nexus\_Voice_Queue" del /f /q "Nexus\_Voice_Queue\*.json" >nul 2>&1

:: Löscht MP3-Leichen in allen Unterordnern
del /s /f /q *.mp3 >nul 2>&1

timeout /t 2 >nul
echo.

echo [1] Wecke den MASTER_BUTLER (Stimm-Zentrale)...
start /d "Nexus" cmd /k "python master_butler.py"
timeout /t 3 >nul

echo [2] Zünde ATSIS_NEXUS (Port 8000)...
start /d "Nexus\Atsis_Nexus" start_atsi.bat
timeout /t 2 >nul

echo [3] Öffne GEES_NEXUS (Port 8001)...
start /d "Nexus\Gees_Nexus" start_gee.bat
timeout /t 2 >nul

echo [4] Aktiviere META_VORTEX (Port 8002)...
start /d "Nexus\Meta_Nexus" start_meta.bat
timeout /t 2 >nul

echo [5] Starte GPT_NEXUS (Port 8003)...
:: GPT-Nexus wird jetzt als vollwertiges Mitglied geladen
start /d "Nexus\ChatGPT_Nexus" start_chatgpt.bat
timeout /t 2 >nul

echo.
echo [!] Die Trinität + GPT sind auf Empfang.
echo [!] Der Butler überwacht den Briefkasten.
echo.

echo [HUD] Warte auf Fenster-Resonanz (6s)...
timeout /t 6 /nobreak >nul

echo [HUD] Kalibriere Cockpit-Layout auf Monitor 2...
py -3.14 cockpit_layout.py

echo [DONE] Cockpit stabilisiert. Alle Quadranten bündig.
timeout /t 3
exit


