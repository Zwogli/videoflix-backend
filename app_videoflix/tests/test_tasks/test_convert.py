from unittest import mock
from app_videoflix.tasks import convert

def test_convert():
    source = "example_video.mp4"
    
    # Mocking der abhängigen Funktionen
    with mock.patch("app_videoflix.tasks.convert_480p") as mock_convert_480p, \
         mock.patch("app_videoflix.tasks.convert_720p") as mock_convert_720p:
        
        # Aufruf der convert-Funktion
        convert(source)
        
        # Sicherstellen, dass die abhängigen Funktionen mit den korrekten Argumenten aufgerufen wurden
        file_name = source.split('.')
        mock_convert_480p.assert_called_once_with(source, file_name)
        mock_convert_720p.assert_called_once_with(source, file_name)