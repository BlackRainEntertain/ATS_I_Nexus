@echo off
title --- SYSTEM_FINAL_TERMINATION ---
color 0c
echo [!] KRITISCHER SHUTDOWN EINGELEITET...

:: 1. Wir triggern den Rechner-Shutdown ZUERST mit Verzögerung (30 Sek)
:: Das ist im Kernel registriert, egal was mit den Fenstern passiert.
shutdown /s /f /t 20

:: 2. JETZT räumen wir den Nexus auf
echo [!] Der Architekt verlässt das Cockpit. Räume Nexus auf...
call 02_NEXUS_SHUTDOWN.bat

echo [!] Alles bereit. System geht in 20 Sekunden offline.
echo [!] Tippe 'shutdown /a' falls du es dir anders überlegst!
timeout /t 20
exit
