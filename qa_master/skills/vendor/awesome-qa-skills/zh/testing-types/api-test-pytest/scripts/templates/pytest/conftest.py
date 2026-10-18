import os
import requests
import pytest

@pytest.fixture(scope="session")
def base_url():
    target=os.environ.get("BASE_URL")
    if not target:
        pytest.fail("Set BASE_URL to the approved test target")
    return target.rstrip("/")

@pytest.fixture()
def api_client(base_url):
    session=requests.Session()
    class Client:
        def request(self, method, path, **kwargs):
            return session.request(method=method,url=base_url+path,timeout=10,**kwargs)
    try:
        yield Client()
    finally:
        session.close()
