Set WshShell = CreateObject("WScript.Shell")
' Chạy file run_server_hidden.bat hoặc gọi trực tiếp pythonw mà không hiện cửa sổ console
WshShell.Run "pythonw """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\app.py""", 0, False
WScript.Sleep 1000
WshShell.Run "http://localhost:5000"
