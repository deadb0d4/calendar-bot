from lib.config import Config


def test_secret_files():
    """
    Checks whether all necessary secret files are present

    Refer to docs for their description and format
    """
    config = Config('./secret')
    assert hasattr(config, 'basic')
    assert hasattr(config, 'bot')
    assert hasattr(config, 'calendar')
    assert hasattr(config, 'credentials')
    assert hasattr(config, 'style')
