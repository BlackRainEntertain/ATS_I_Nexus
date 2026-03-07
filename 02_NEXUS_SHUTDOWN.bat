@echo off
title --- NEXUS_SHUTDOWN_v6 ---
color 0c
echo [!] Aktiviere Python-Radiergummi...
py nexus_kill.py
timeout /t 5
exit