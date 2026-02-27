@echo off
title --- RESUME_VOICE ---
color 0a
echo [SYSTEM] Nexus-Stimme nimmt den Faden wieder auf...
:: taut alle schlafenden PowerShell-Instanzen wieder auf
powershell -Command "Get-Process powershell | Resume-Process" >nul 2>&1
echo [RESUME] Audio-Stream fliesst wieder.
timeout /t 2 >nul
exit
