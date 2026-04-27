import pytest
from copy import deepcopy

from fastapi.testclient import TestClient

from src import app as app_module

initial_activities = deepcopy(app_module.activities)
client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activity_state():
    app_module.activities.clear()
    app_module.activities.update(deepcopy(initial_activities))
    yield
