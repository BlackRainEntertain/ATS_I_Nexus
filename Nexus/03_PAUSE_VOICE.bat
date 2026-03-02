@echo off
title --- PAUSE_VOICE ---
color 0e
echo [SYSTEM] Erzeuge Brems-Signal...
echo PAUSE > "%~dp0NEXUS_PAUSE.tmp"
:: Wir killen die aktuelle PS, damit Ruhe ist - der Butler wartet aber!
taskkill /f /im powershell.exe >nul 2>&1
echo [PAUSE] Butler hält die Wacht.
timeout /t 2 >nul
exit
