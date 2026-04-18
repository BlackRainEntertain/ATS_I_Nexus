@echo off
cd /d "C:\Users\René\Desktop\LM Projekte"
title NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION
color 0b

echo [!] Komplette System-Reinigung (Tabula Rasa)...
:: Killt den Titan-Butler gezielt über seinen Fenstertitel
taskkill /F /FI "WINDOWTITLE eq AUDIO_MASTER_BUTLER_V43.8_TITAN*" /T >nul 2>&1
:: Killt alle Python-Instanzen
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
:: Räumt hängende Explorer-Zombies auf
taskkill /F /IM explorer.exe /FI "WINDOWTITLE eq LM Projekte" >nul 2>&1
taskkill /F /FI "WINDOWTITLE ne NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION" /IM cmd.exe /T >nul 2>&1
timeout /t 2 >nul

echo [!] Bereinige EXKLUSIV die Voice-Queue UND den Tresor...
:: Harter Schnitt: Löscht alle Dateien (*.*), nicht nur .json
if exist "Nexus\_Voice_Queue" del /f /s /q "Nexus\_Voice_Queue\*.*" >nul 2>&1
if exist "Nexus\_Active_Ticket" del /f /s /q "Nexus\_Active_Ticket\*.*" >nul 2>&1

:: Spezifische Vernichtung der Blockade-Dateien im Hauptverzeichnis
if exist "Nexus\NEXUS_PAUSE.tmp" del /f /q "Nexus\NEXUS_PAUSE.tmp" >nul 2>&1
if exist "Nexus\NEXUS_NEXT.tmp" del /f /q "Nexus\NEXUS_NEXT.tmp" >nul 2>&1
if exist "NEXUS_PAUSE.tmp" del /f /q "NEXUS_PAUSE.tmp" >nul 2>&1

:: Säuberung des Audio-Caches (optional, falls du dort auch aufräumen willst)
:: if exist "Nexus\_Audio_Cache" del /f /q "Nexus\_Audio_Cache\*.mp3" >nul 2>&1

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

:: JETZT DER FINALE AKT (Wiederbelebung der Services)
echo [FINAL] Aktiviere das Gehör via Launcher-VBS...
start "" "C:\Users\René\Desktop\LM Projekte\Nexus_Service\Gee_Ear_Launcher.vbs"

echo [SERVICE] Aktiviere Explorer-Exorzist...
start "" "C:\Users\René\Desktop\LM Projekte\Nexus_Service\Gee_Exorcist_Launcher.vbs"

echo [DONE] Cockpit stabilisiert. Resonanz auf 100%.
timeout /t 3 >nul
exit