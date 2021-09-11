from lib.config import Config


def test_secret_files():
    """
    Checks whether all necessary secret files are present

    Refer to docs for their description and format
    """
    config = Config("./secret")
    properties = ["basic", "bot", "calendar", "credentials", "style"]
    for prop in properties:
        assert hasattr(config, prop)
