Set WshShell = CreateObject("WScript.Shell")
' Die 7 minimiert das Fenster sofort, damit es nicht dominiert
WshShell.Run "cmd /k py ""C:\Users\René\Desktop\LM Projekte\Nexus_Service\explorer_exorcist.py""", 7, False
