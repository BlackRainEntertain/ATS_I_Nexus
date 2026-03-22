@echo off
title --- PAUSE_VOICE ---
color 0e
echo [SYSTEM] Erzeuge Brems-Signal...
echo PAUSE > "%~dp0NEXUS_PAUSE.tmp"
echo [PAUSE] Butler hält die Wacht.
timeout /t 2 >nul
exit
