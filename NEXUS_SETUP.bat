@echo off
title --- NEXUS SETUP: TITAN-INSTALLER v2.0 ---
color 0b

echo [!] Erkenne Python-Umgebung...
py --version
py -m pip install --upgrade pip
timeout /t 1 >nul

echo [!] Scanne Nexus-Architektur nach Abhaengigkeiten...

:: 1. Scannt alle KI-Ordner in Nexus/
for /d %%i in (Nexus\*) do (
    if exist "%%i\requirements.txt" (
        echo [+] Gefunden: %%i... installiere.
        py -m pip install -r "%%i\requirements.txt"
    )
)

:: 2. Scannt den Sprach-Dienst
if exist "Nexus_Service\requirements.txt" (
    echo [+] Installiere Ohr-Resonanz (Nexus_Service)...
    py -m pip install -r "Nexus_Service\requirements.txt"
)

:: 3. Lokale Haupt-Requirements (Falls im Root noch was liegt)
if exist "requirements.txt" (
    py -m pip install -r requirements.txt
)

echo.
echo [OK] Alle Schrauben im gesamten System sind festgezogen.
pause
exit
