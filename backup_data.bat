@echo off

REM Set the environment for Django
REM This assumes you're using a virtual environment
SET VENV_PATH=C:\Dev\backend\08-videoflix\videoflix-backend
SET PROJECT_PATH=C:\Dev\backend\08-videoflix\videoflix-backend

REM Activate the virtual environment
CALL %VENV_PATH%\Scripts\activate

REM Navigate to the Django project directory
cd %PROJECT_PATH%

REM Create a backup directory if it doesn't exist
if not exist backups mkdir backups

REM Export data from app_videoflix.GlobalVideo and app_videoflix.LocalVideo
python manage.py dumpdata app_videoflix.GlobalVideo app_videoflix.LocalVideo --output=backups/videoflix_backup.json --indent 4

REM Export data from CustomUser model
python manage.py dumpdata app_authentication.CustomUser --output=backups/customuser_backup.json --indent 4

REM Combine all JSON files into one file (Optional)
REM This is a simple concatenation, you might want to merge them programmatically in Django if needed
copy /b backups\videoflix_backup.json+backups\customuser_backup.json backups\full_backup.json

REM Deactivate the virtual environment
deactivate

@echo Backup completed successfully!
pause