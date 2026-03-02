@echo off
title --- RESUME_VOICE ---
color 0a
echo [SYSTEM] Lösche Brems-Signal...
if exist "%~dp0NEXUS_PAUSE.tmp" del "%~dp0NEXUS_PAUSE.tmp"
echo [RESUME] Der Butler darf weitermachen.
timeout /t 2 >nul
exit
