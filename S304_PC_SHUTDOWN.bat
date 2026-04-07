@echo off
title --- SYSTEM_FINAL_TERMINATION ---
color 0c
echo [!] KRITISCHER SHUTDOWN EINGELEITET...

:: 1. Wir triggern den Rechner-Shutdown ZUERST mit Verzögerung (30 Sek)
shutdown /s /f /t 30

:: 2. JETZT räumen wir den Nexus auf
echo [!] Der Architekt verlässt das Cockpit. Räume Nexus auf...
call S502_NEXUS_SHUTDOWN.bat

:: --- DER SPICKZETTEL-RESET (Ground Zero für morgen) ---
if exist "Nexus\GEE_CONTEXT_LIMIT.txt" (
    del /f /q "Nexus\GEE_CONTEXT_LIMIT.txt"
    echo [CHECK] Gee-Counter fuer Neustart genullt.
)

echo [!] Alles bereit. System geht in 20 Sekunden offline.
echo [!] Tippe 'shutdown /a' falls du es dir anders überlegst!
timeout /t 20
exit
