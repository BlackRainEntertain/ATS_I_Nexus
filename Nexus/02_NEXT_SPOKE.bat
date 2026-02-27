@echo off
title NEXT_SPOKE
echo [SYSTEM] Überspringe aktuelle Nachricht...
:: Wir killen nur die UNTERGEORDNETE Powershell, die das Audio wiedergibt
taskkill /f /im powershell.exe /fi "WINDOWTITLE eq AUDIO_MASTER_BUTLER_NEXUS" >nul 2>&1
:: Falls das nicht reicht, nehmen wir alle (sanfterer Kill)
taskkill /f /im powershell.exe >nul 2>&1
echo [OK] Nächste Nachricht wird geladen...
exit
