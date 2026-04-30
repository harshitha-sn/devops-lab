
import pytest
from unittest.mock import patch
import app as flask_app

@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with patch("app.r") as mock_redis:
        mock_redis.incr.return_value = 1
        mock_redis.get.return_value = "1"
        with flask_app.app.test_client() as client:
            yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert "visits" in data
    assert "hostname" in data


def test_reset(client):
    res = client.post("/reset")
    assert res.status_code == 200
    assert res.get_json()["visits"] == 0


def test_reset_method_not_allowed(client):
    res = client.get("/reset")
    assert res.status_code == 405


def test_stats(client):
    res = client.get("/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert "visits" in data
    assert "hostname" in data
    assert "redis_host" in data
