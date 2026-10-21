@echo off
chcp 65001 >nul
title GOOGLE_AI_MODE_RECOVERY_INJECTOR
color 0b

echo =======================================================================
echo [!] Starte manuellen Clipboard-Injektor...
echo =======================================================================
timeout /t 1 >nul

py injector.py
pause
exit
