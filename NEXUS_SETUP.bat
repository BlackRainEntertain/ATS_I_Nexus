@echo off
title --- NEXUS SETUP: INSTALLING BOLTS & SCREWS ---
color 0b
echo [!] Starte Installation der Nexus-Module...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
echo.
echo [OK] Alle Module sind bereit. Gee kann jetzt hoeren.
pause
