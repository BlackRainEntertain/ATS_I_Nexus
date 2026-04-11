@echo off
title S106_ON_LAVA_RESONANZ
cd /d "%~dp0"
echo [VISUAL] Zünde Lava-Resonanz...
start "" /d "Nexus\System_Visuals" pythonw lava_stream.py
timeout /t 2 >nul
echo [PILOT] Positioniere Visuals im Orbit...
python "Nexus\System_Visuals\lava_pilot.py"
exit

