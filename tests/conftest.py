import pytest
import sys
import os
from freezegun import freeze_time

# add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# enable freezegun for all tests
@pytest.fixture(scope="session")
def freeze_session():
    with freeze_time("2000-01-01"):
        yield

# enable freezegun for all tests
@pytest.fixture(autouse=True)
def freeze_module(freeze_session):
    pass

# enable httpretty for all tests
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    httpretty.enable()
    yield
    httpretty.disable()
