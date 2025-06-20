import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from main import app

client = TestClient(app)

def test_plan_trajectory_valid():
    response = client.post("/plan", json={
        "wall": {"width": 5.0, "height": 5.0},
        "obstacles": [{"x": 1.0, "y": 1.0, "width": 0.25, "height": 0.25}]
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "x" in data[0] and "y" in data[0]

def test_plan_trajectory_invalid_wall():
    response = client.post("/plan", json={
        "wall": {"width": -1.0, "height": 5.0},
        "obstacles": []
    })
    assert response.status_code == 400

def test_get_trajectory_not_found():
    response = client.get("/trajectory/999999")
    assert response.status_code == 404

def test_save_and_get_trajectory():
    # Save a sample trajectory
    sample_trajectory = [
        {"x": 0, "y": 0},
        {"x": 1, "y": 0},
        {"x": 1, "y": 1}
    ]
    response = client.post("/trajectory", json={
        "wall": {"width": 5.0, "height": 5.0},
        "obstacles": [{"x": 1.0, "y": 1.0, "width": 0.25, "height": 0.25}],
        "path": sample_trajectory
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    trajectory_id = data["id"]

    # Get the saved trajectory
    response = client.get(f"/trajectory/{trajectory_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["wall"]["width"] == 5.0
    assert data["wall"]["height"] == 5.0
    assert isinstance(data["path"], list)
    assert len(data["path"]) == 3

def test_list_trajectories():
    response = client.get("/trajectories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_response_time_plan_trajectory():
    import time
    start = time.time()
    response = client.post("/plan", json={
        "wall": {"width": 5.0, "height": 5.0},
        "obstacles": []
    })
    duration = time.time() - start
    assert response.status_code == 200
    assert duration < 1.0  # response time less than 1 second
