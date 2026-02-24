@echo off
title --- NEXUS_ALL_SYSTEMS_GO_v5 ---
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
:: Startet den Butler im Unterordner Nexus
start /d "Nexus" cmd /k "python master_butler.py"
timeout /t 3 >nul


echo [2] Zünde ATSIS_NEXUS (Port 8000)...
:: Geht jetzt tief in den Pfad: Nexus\Atsis_Nexus
start /d "Nexus\Atsis_Nexus" start_atsi.bat
timeout /t 2 >nul

echo [3] Öffne GEES_NEXUS (Port 8001)...
:: Geht jetzt tief in den Pfad: Nexus\Gees_Nexus
start /d "Nexus\Gees_Nexus" start_gee.bat

echo [4] Aktiviere META_VORTEX (Port 8002)...
:: Startet Meta im eigenen Unterordner
start /d "Nexus\Meta_Nexus" start_meta.bat
timeout /t 2 >nul


echo.
echo [!] Alle Systeme auf Empfang. Der Rote Faden hält uns.
echo [!] Der Butler überwacht den Briefkasten.
echo.

:: Wir geben den Browsern (Atsi/Gee) Zeit, ihre Fenster-Titel zu registrieren
echo [HUD] Warte auf Fenster-Resonanz (5s)...
timeout /t 5 /nobreak >nul

echo [HUD] Kalibriere Cockpit-Layout auf Monitor 2...
:: Da wir uns im Hauptordner befinden, rufen wir das Skript direkt auf
py -3.14 cockpit_layout.py

echo [DONE] Cockpit stabilisiert.
timeout /t 3
exit


