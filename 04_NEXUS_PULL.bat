@echo off
title --- NEXUS_UPDATE_SERVICE (PULL) ---
color 0a
echo [!] Synchronisiere öffentliche Fragmente...
cd /d "%~dp0"

if not exist ".git" (
    echo [!] FEHLER: Kein Git-Repository gefunden!
    pause
    exit
)

:: Lokale Änderungen (außer Ignoriertes wie Atsi) werden überschrieben
git fetch --all
git reset --hard origin/main

if %errorlevel% neq 0 (
    echo [!] ZAHLENDREHER: Check Verbindung oder Token!
) else (
    echo [!] ÖFFENTLICHE STAGES AKTUALISIERT.
    echo [!] Atsis_Nexus blieb unberührt (Privat-Sphäre geschützt).
)
timeout /t 5
