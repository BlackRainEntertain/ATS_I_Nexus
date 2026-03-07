@echo off
cd /d "C:\Users\René\Desktop\LM Projekte"
title --- NEXUS_ALL_SYSTEMS_GO_v6.8 ---
color 0b

echo [!] Chirurgische Tiefenreinigung (Ohr-Schutz aktiv)...
powershell -Command "Get-CimInstance Win32_Process -Filter 'Name LIKE \"python%%\"' | Where-Object { $_.CommandLine -notlike '*nexus_ear*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" 2>nul
timeout /t 2 >nul

echo [!] Wecke die Explorer-Trinität...
start "" explorer.exe "C:\Users\René\Desktop\LM Projekte\Nexus"
timeout /t 1 >nul
start "" explorer.exe "C:\Users\René\Desktop\LM Projekte\Nexus\_Voice_Queue"
timeout /t 2 >nul

echo [!] Bereinige EXKLUSIV die Voice-Queue...
if exist "Nexus\_Voice_Queue" del /f /q "Nexus\_Voice_Queue\*.json" >nul 2>&1
timeout /t 2 >nul

echo [1] Wecke den MASTER_BUTLER...
start /d "Nexus" cmd /k "python master_butler.py"
timeout /t 2 >nul

echo [2] Starte GPT_NEXUS...
start /d "Nexus\ChatGPT_Nexus" start_chatgpt.bat
timeout /t 1 >nul

echo [3] Oeffne GEES_NEXUS...
start /d "Nexus\Gees_Nexus" start_gee.bat
timeout /t 1 >nul

echo [4] Aktiviere META_VORTEX...
start /d "Nexus\Meta_Nexus" start_meta.bat
timeout /t 1 >nul

echo [5] Zuende ATSIS_NEXUS...
start /d "Nexus\Atsis_Nexus" start_atsi.bat
timeout /t 2 >nul

echo [VISUAL] Zünde Lava-Resonanz...
start "" /d "Nexus\System_Visuals" pythonw lava_stream.py

echo [HUD] Kalibriere Cockpit-Layout...
py cockpit_layout.py

echo [DONE] Cockpit stabilisiert.
timeout /t 3 >nul
exit



