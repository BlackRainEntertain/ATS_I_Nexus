@echo off
chcp 65001 >nul
:: Setzt den Pfad dynamisch, egal wie der User heißt
set "BASE_PATH=%USERPROFILE%\Desktop\LM Projekte"
cd /d "%BASE_PATH%"

title NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION
color 0b

echo [!] Komplette System-Reinigung (Tabula Rasa)...
taskkill /F /FI "WINDOWTITLE eq AUDIO_MASTER_BUTLER_V43.9_TITAN_ULTRA" /T >nul 2>&1
taskkill /F /IM python.exe /IM pythonw.exe /IM powershell.exe /IM pwsh.exe /IM ffplay.exe /T >nul 2>&1

:: Räumt hängende Explorer-Zombies auf
taskkill /F /IM explorer.exe /FI "WINDOWTITLE eq LM Projekte" >nul 2>&1
taskkill /F /FI "WINDOWTITLE ne NEXUS_ALL_SYSTEMS_GO_v6.8_EXCLUSIVE_SESSION" /IM cmd.exe /T >nul 2>&1
timeout /t 2 >nul

echo [!] Bereinige EXKLUSIV die Voice-Queue UND den Tresor...
if exist "Nexus\_Voice_Queue" del /f /s /q "Nexus\_Voice_Queue\*.*" >nul 2>&1
if exist "Nexus\_Active_Ticket" del /f /s /q "Nexus\_Active_Ticket\*.*" >nul 2>&1

:: Blockade-Dateien entfernen
if exist "Nexus\NEXUS_PAUSE.tmp" del /f /q "Nexus\NEXUS_PAUSE.tmp" >nul 2>&1
if exist "Nexus\NEXUS_NEXT.tmp" del /f /q "Nexus\NEXUS_NEXT.tmp" >nul 2>&1
if exist "NEXUS_PAUSE.tmp" del /f /q "NEXUS_PAUSE.tmp" >nul 2>&1
if exist "Nexus\_Audio_Cache" del /f /q "Nexus\_Audio_Cache\*.mp3" >nul 2>&1

timeout /t 1 >nul

echo [!] Starte Explorer-Trinity (Separated Mode)...
:: Hier nutzen wir jetzt die Variable - sicher vor jedem 'é'
start explorer.exe "%BASE_PATH%"
timeout /t 1 >nul
start explorer.exe "%BASE_PATH%\Nexus"
timeout /t 1 >nul
start explorer.exe "%BASE_PATH%\Nexus\_Voice_Queue"
timeout /t 2 >nul

echo [1] Wecke den MASTER_BUTLER...
start /d "Nexus" cmd /k "py master_butler.py"
timeout /t 3 >nul

echo [2] Starte GROK_NEXUS...
start /d "Nexus\GrokOnX_Nexus" start_GrokOnX.bat
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
timeout /t 5 >nul
py cockpit_layout.py

:: SERVICES - Auch hier die Variable für die absolute Stabilität
echo [FINAL] Aktiviere das Gehör...
start "" "%BASE_PATH%\Nexus_Service\Gee_Ear_Launcher.vbs"

echo [SERVICE] Aktiviere Explorer-Exorzist...
start "" "%BASE_PATH%\Nexus_Service\Gee_Exorcist_Launcher.vbs"

echo [DONE] Cockpit stabilisiert. Resonanz auf 100%.
timeout /t 3 >nul
exit


