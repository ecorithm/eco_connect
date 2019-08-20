from importlib.machinery import SourceFileLoader
import requests


class MockResponse:
    status_code = 200


def mock_get(*args, **kwargs):
    return MockResponse()


def test_validate_credentials(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_get)
    SourceFileLoader("__main__", "eco_connect/__init__.py").load_module()
