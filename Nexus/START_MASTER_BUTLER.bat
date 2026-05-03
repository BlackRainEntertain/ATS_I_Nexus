@echo off
title AUDIO_MASTER_BUTLER
pushd "%~dp0"
echo [SYSTEM] Warte auf Tickets im Briefkasten...
py master_butler.py
popd
pause
