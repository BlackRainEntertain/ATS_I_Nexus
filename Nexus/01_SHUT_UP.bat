@echo off
title PANIK_KNOPF
echo [SYSTEM] Butler wird zum Schweigen gebracht...
taskkill /f /im powershell.exe /t >nul 2>&1
echo [OK] Stille wiederhergestellt.
timeout /t 2 >nul
