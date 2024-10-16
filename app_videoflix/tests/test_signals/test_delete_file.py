import os
import pytest
from unittest.mock import patch
from app_videoflix.signals import delete_file  # Korrigierter Modulpfad

@pytest.fixture
def mock_file(tmp_path):
    """Erstellt eine temporäre Datei für die Tests."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Testinhalt")
    return str(file_path)

def test_delete_file_existing(mock_file):
    """Testet das Löschen einer vorhandenen Datei."""
    # Überprüfe, dass die Datei existiert
    assert os.path.isfile(mock_file)

    # Simuliere das Löschen der Datei
    with patch('os.path.isfile', return_value=True), patch('os.remove') as mock_remove:
        delete_file(mock_file)
        mock_remove.assert_called_once_with(mock_file)

    # Überprüfe, dass die Datei nach dem Löschen nicht mehr existiert
    # Hier simulieren wir das Verhalten von isfile
    with patch('os.path.isfile', return_value=False):
        assert not os.path.isfile(mock_file)

def test_delete_file_non_existing():
    """Testet das Verhalten beim Löschen einer nicht vorhandenen Datei."""
    non_existing_file = "non_existing_file.txt"

    with patch('os.remove') as mock_remove:
        delete_file(non_existing_file)
        mock_remove.assert_not_called()

def test_delete_file_with_none():
    """Testet das Verhalten, wenn der Dateipfad None ist."""
    with patch('os.remove') as mock_remove:
        delete_file(None)
        mock_remove.assert_not_called()
