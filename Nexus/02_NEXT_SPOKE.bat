@echo off
title NEXT_SPOKE
echo [SYSTEM] Überspringe aktuelle Nachricht...
:: Das Signal-File für den Butler
echo NEXT > "%~dp0NEXUS_NEXT.tmp"

:: FORCE-CLOSE ohne Rückfrage (Das 'echo j |' fängt das J/N ab)
echo j | taskkill /f /im powershell.exe /t >nul 2>&1

echo [OK] Nächste Nachricht wird geladen...
timeout /t 1 >nul
exit

