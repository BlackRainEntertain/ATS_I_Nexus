@echo off
title NEXT_SPOKE
echo [SYSTEM] Überspringe aktuelle Nachricht...
:: Wir legen nur das Signal-File ab - der Butler sieht es und schliesst die PS sauber!
echo NEXT > "%~dp0NEXUS_NEXT.tmp"
echo [OK] Nächste Nachricht wird geladen...
timeout /t 1 >nul
exit

