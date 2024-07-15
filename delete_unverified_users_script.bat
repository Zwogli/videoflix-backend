@echo off

set PYTHON_EXECUTABLE="C:\Users\Zwogli\AppData\Local\Programs\Python\Python312\python.exe"
set SCRIPT_FILE="C:\Dev\backend\08-videoflix\videoflix-backend\app_authentication\management\commands\delete_unverified_users.py"

%PYTHON_EXECUTABLE% %SCRIPT_FILE%

pause