"""Test that paths correspand to project structure"""
from app.helpers.paths import ROOT_DIR, DATA_DIR


def test_paths():
    """Test ROOT_DIR and DATA_DIR path"""
    assert 'app' == str(ROOT_DIR).split("/")[-1]
    assert ['app', 'data'] == str(DATA_DIR).split("/")[-2:]
