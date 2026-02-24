@echo off
title --- NEXUS_SHUTDOWN_v6 ---
color 0c
echo [!] Aktiviere Python-Radiergummi...
py -3.14 nexus_kill.py
timeout /t 3
exit
