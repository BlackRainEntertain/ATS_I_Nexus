@echo off
title --- RESUME_VOICE ---
color 0a

:: Prüfe, ob eine Pause aktiv ist. Wenn nicht, beende sofort ohne Aktion.
if not exist "%~dp0NEXUS_PAUSE.tmp" (
    exit
)

echo [SYSTEM] Lösche Brems-Signal...
del "%~dp0NEXUS_PAUSE.tmp"
echo [RESUME] Der Butler darf weitermachen.
timeout /t 2 >nul
exit

