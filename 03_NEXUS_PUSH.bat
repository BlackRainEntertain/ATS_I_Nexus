@echo off
title --- NEXUS_GITHUB_SYNC_V1 ---
color 0b
echo [!] Scanne Matrix auf Veraenderungen...
cd /d "%~dp0"

:: Check ob Git initialisiert ist
if not exist ".git" (
    echo [!] Initialisiere lokales Repository...
    git init
    git remote add origin https://github.com
)

git add .
set current_date=%date% %time%
git commit -m "Snapshot: %current_date% (Layout, Trinity & Backups-Safe)"
echo [!] Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo [!] ZAHLENDREHER: Check Login/Token!
    pause
) else (
    echo [!] SYNCHRONISATION ERFOLGREICH.
    timeout /t 5
)
