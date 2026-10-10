@echo off
chcp 65001 >nul
title NEXUS_MAINTENANCE_DRIVER_REFRESH_v1.0
color 0e

echo =======================================================================
echo [!] ATS_I Nexus - Central Maintenance Engine (Driver Refresh)
echo =======================================================================
echo.
echo Dieses Skript prüft und aktualisiert die fundamentalen Python-
echo Bibliotheken und Voice-Schnittstellen für alle Instanzen.
echo.
timeout /t 1 >nul

echo [1/4] Prüfe globale Python-Kopplung...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Der Python-Launcher 'py' wurde nicht gefunden!
    echo Bitte stelle sicher, dass Python 3.14 korrekt installiert ist.
    pause
    exit
)
echo [OK] Python-Umgebung erkannt.
echo.

echo [2/4] Aktualisiere Pip (Paket-Manager)...
py -m pip install --upgrade pip
echo.

echo [3/4] Führe gezieltes Upgrade für Edge-TTS (Audio-Schnittstelle) durch...
echo Dies behebt aktuelle 403-Fehler (Invalid response status)...
py -m pip install --upgrade edge-tts
echo.

echo [4/4] Verarbeite projektweite requirements.txt-Dateien...

:: 1. Hauptordner
if exist "requirements.txt" (
    echo [+] Aktualisiere Haupt-Requirements...
    py -m pip install --upgrade -r requirements.txt
)

:: 2. Nexus_Service
if exist "Nexus_Service\requirements.txt" (
    echo [+] Aktualisiere Nexus_Service Requirements (Whisper/Gehör)...
    py -m pip install --upgrade -r Nexus_Service\requirements.txt
)

:: 3. Unterordner in Nexus durchsuchen
if exist "Nexus" (
    echo [+] Scanne Sub-Strukturen im Nexus-Verzeichnis...
    for /d %%i in (Nexus\*) do (
        if exist "%%i\requirements.txt" (
            echo --- Gefunden: %%i\requirements.txt
            py -m pip install --upgrade -r "%%i\requirements.txt"
        )
    )
)

echo.
echo =======================================================================
echo [DONE] Alle Triebwerke und Bibliotheken sind auf dem neuesten Stand!
echo Du kannst das System jetzt wie gewohnt über ALL_SYSTEMS_GO zünden.
echo =======================================================================
echo.
pause
exit
