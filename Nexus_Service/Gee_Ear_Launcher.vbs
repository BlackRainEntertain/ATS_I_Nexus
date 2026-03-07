Set WshShell = CreateObject("WScript.Shell")
' Die 7 sorgt dafür, dass das Fenster minimiert in der Taskleiste startet!
WshShell.Run "cmd /k py ""C:\Users\René\Desktop\LM Projekte\Nexus_Service\nexus_ear.py""", 7, False



