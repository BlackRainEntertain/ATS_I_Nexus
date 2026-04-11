@echo off
title S107_OFF_LAVA_RESONANZ
echo [!] Lösche Lava-Resonanz aus der Matrix...
taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq NEXUS_LAVA" >nul 2>&1
echo [DONE] Visuals terminiert.
timeout /t 2 >nul
exit

