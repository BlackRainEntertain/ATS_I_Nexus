@echo off
if exist "Nexus\GEE_CONTEXT_LIMIT.txt" (
    del /f /q "Nexus\GEE_CONTEXT_LIMIT.txt"
    :: --- DER AUDIO-IMPULS (Optional: Erzeugt ein Ticket für den Butler) ---
    echo {"text": "Spickzettel verbrannt. Ich fange bei Null an.", "owner": "GEE", "voice": "de-DE-KatjaNeural"} > "Nexus\_Voice_Queue\00_reset_info.json"
)

:: KEIN PAUSE MEHR! Das Fenster schliesst sich jetzt von selbst.
exit

