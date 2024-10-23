import subprocess
import pytest
from unittest import mock
from app_videoflix.tasks import run_ffmpeg_command

def test_run_ffmpeg_command_success():
    cmd = ['ffmpeg', '-i', 'input.mp4', '-s', 'hd480', 'output.mp4']

    # Simuliere, dass subprocess.run erfolgreich ausgeführt wird
    with mock.patch("subprocess.run") as mock_run:
        with mock.patch("app_videoflix.tasks.logger.info") as mock_logger:
            run_ffmpeg_command(cmd)

            # Überprüfe, dass subprocess.run mit den richtigen Argumenten aufgerufen wurde
            mock_run.assert_called_once_with(cmd, check=True)

            # Überprüfe, dass der Logger die Erfolgsmeldung protokolliert hat
            mock_logger.assert_called_once_with(f'FFmpeg command executed successfully: {" ".join(cmd)}')

def test_run_ffmpeg_command_failure():
    cmd = ['ffmpeg', '-i', 'input.mp4', '-s', 'hd480', 'output.mp4']

    # Simuliere, dass subprocess.run eine CalledProcessError auslöst
    with mock.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, cmd)) as mock_run:
        with mock.patch("app_videoflix.tasks.logger.error") as mock_logger:
            with pytest.raises(subprocess.CalledProcessError):
                run_ffmpeg_command(cmd)

            # Überprüfe, dass subprocess.run mit den richtigen Argumenten aufgerufen wurde
            mock_run.assert_called_once_with(cmd, check=True)

            # Überprüfe, dass der Logger die Fehlermeldung protokolliert hat
            mock_logger.assert_called_once_with(f'FFmpeg command failed: {" ".join(cmd)}; Error: {mock_run.side_effect}')
