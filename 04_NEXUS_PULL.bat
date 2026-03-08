@echo off
title --- NEXUS_UPDATE_SERVICE (PULL_GUARD) ---
color 0c
cd /d "%~dp0"

:: --- ARCHITEKTEN-SCHUTZ ---
if exist "ARCHITECT_LOCKED.txt" (
    echo [!] ZUGRIFF VERWEIGERT: ARCHITEKTEN-SPERRE AKTIV.
    echo [!] Ein Pull wuerde deine lokalen Dev-Stages ueberschreiben.
    echo [!] Loesche 'ARCHITECT_LOCKED.txt' fuer ein Force-Update.
    timeout /t 10
    exit
)

echo [!] Synchronisiere oeffentliche Fragmente...
if not exist ".git" (
    echo [!] FEHLER: Kein Git-Repository gefunden!
    pause
    exit
)

:: Lokale Aenderungen werden ueberschrieben (ausser Ignoriertes)
git fetch --all
git reset --hard origin/main

if %errorlevel% neq 0 (
    echo [!] ZAHLENDREHER: Check Verbindung oder Token!
) else (
    echo [!] OEFFENTLICHE STAGES AKTUALISIERT.
    echo [!] Atsis_Nexus blieb unberuehrt.
)
timeout /t 5
