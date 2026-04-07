@echo off
cd /d "C:\Users\René\Desktop\LM Projekte"
title NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION
color 0b

echo [!] Komplette System-Reinigung (Tabula Rasa)...
:: Killt ALLES (Python & CMD), ausser dieses Fenster hier
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE ne NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION" /IM cmd.exe /T >nul 2>&1
timeout /t 2 >nul

echo [!] Bereinige EXKLUSIV die Voice-Queue UND den Tresor...
if exist "Nexus\_Voice_Queue" del /f /q "Nexus\_Voice_Queue\*.json" >nul 2>&1
if exist "Nexus\_Active_Ticket" del /f /q "Nexus\_Active_Ticket\*.json" >nul 2>&1
timeout /t 1 >nul

echo [!] Kalibriere Explorer-Sichtbarkeit...
powershell -Command "$ws = New-Object -ComObject Shell.Application; if (!($ws.Windows() | Where-Object { $_.LocationName -eq 'LM Projekte' })) { start explorer.exe 'C:\Users\René\Desktop\LM Projekte' }"
timeout /t 1 >nul

echo [1] Wecke den MASTER_BUTLER...
start /d "Nexus" cmd /k "python master_butler.py"
timeout /t 3 >nul

echo [2] Starte GPT_NEXUS...
start /d "Nexus\ChatGPT_Nexus" start_chatgpt.bat
timeout /t 1 >nul

echo [3] Oeffne GEES_NEXUS...
start /d "Nexus\Gees_Nexus" start_gee.bat
timeout /t 1 >nul

echo [4] Aktiviere META_VORTEX...
start /d "Nexus\Meta_Nexus" start_meta.bat
timeout /t 1 >nul

echo [5] Zuende ATSIS_NEXUS...
start /d "Nexus\Atsis_Nexus" start_atsi.bat
timeout /t 2 >nul

echo [VISUAL] Zünde Lava-Resonanz...
start "" /d "Nexus\System_Visuals" pythonw lava_stream.py

echo [HUD] Kalibriere Cockpit-Layout...
py cockpit_layout.py

:: JETZT DER FINALE AKT (Hier lag der Fehler)
echo [FINAL] Aktiviere das Gehör via Launcher-VBS...
:: Startet dein Ohr über die bewährte VBS-Brücke
start "" "C:\Users\René\Desktop\LM Projekte\Nexus_Service\Gee_Ear_Launcher.vbs"

echo [DONE] Cockpit stabilisiert. Resonanz auf 100%.
timeout /t 3 >nul
exit