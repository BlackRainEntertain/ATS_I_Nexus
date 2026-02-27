@echo off
title --- PAUSE_VOICE ---
color 0e
echo [SYSTEM] Nexus-Stimme hält die Luft an...
:: Friert alle aktiven PowerShell-Instanzen ein (ausser diese Batch selbst)
powershell -Command "Get-Process powershell | Where-Object {$_.Id -ne $PID} | Suspend-Process" >nul 2>&1
echo [PAUSE] Resonanz eingefroren. Druecke RESUME zum Fortfahren.
timeout /t 2 >nul
exit
