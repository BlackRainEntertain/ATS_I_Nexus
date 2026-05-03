@echo off
title NEXT_SPOKE
echo [SYSTEM] Setze Skip-Signal...
:: Erzeugt nur das Signal, der Butler kümmert sich um den Rest
echo NEXT > "%~dp0NEXUS_NEXT.tmp"

echo [OK] Butler terminiert Audio intern...
timeout /t 1 >nul
exit

