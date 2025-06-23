from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from models import TrajectoryCreate, TrajectoryInDB, TrajectoryPoint, PlanInput
import sys
import os
sys.path.append(os.path.dirname(__file__))

from db import get_connection, init_db
from typing import List
import json
from datetime import datetime
import asyncio

router = APIRouter()

# Initialize DB on startup
init_db()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/trajectory")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back received data or handle commands
            await manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/plan", response_model=List[TrajectoryPoint])
def plan_trajectory(data: PlanInput):
    """
    Generates a zig-zag path for wall coverage while avoiding rectangular obstacles.
    """
    wall = data.wall
    obstacles = data.obstacles

    if wall.width <= 0 or wall.height <= 0:
        raise HTTPException(status_code=400, detail="Wall dimensions must be positive numbers")

    def is_inside_obstacle(x: float, y: float) -> bool:
        for obs in obstacles:
            if (obs.x <= x <= obs.x + obs.width) and (obs.y <= y <= obs.y + obs.height):
                return True
        return False

    path = []
    step = 0.5  # resolution in meters
    y = 0.0
    direction = 1  # left-to-right or right-to-left

    while y <= wall.height:
        if direction == 1:
            x_range = [x * step for x in range(int(wall.width / step) + 1)]
        else:
            x_range = [x * step for x in reversed(range(int(wall.width / step) + 1))]

        for x in x_range:
            if not is_inside_obstacle(x, y):
                path.append(TrajectoryPoint(x=x, y=y))
            # else skip this point as it's inside an obstacle
        y += step
        direction *= -1

    return path

@router.post("/trajectory", response_model=TrajectoryInDB)
def save_trajectory(data: TrajectoryCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trajectories (wall_width, wall_height, obstacles, trajectory)
        VALUES (?, ?, ?, ?)
    """, (
        data.wall.width,
        data.wall.height,
        json.dumps([obs.dict() for obs in data.obstacles]),
        json.dumps([point.dict() for point in data.path])
    ))
    conn.commit()
    traj_id = cursor.lastrowid
    cursor.execute("SELECT * FROM trajectories WHERE id = ?", (traj_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return TrajectoryInDB(
            id=row["id"],
            wall={"width": row["wall_width"], "height": row["wall_height"]},
            obstacles=json.loads(row["obstacles"]),
            path=json.loads(row["trajectory"]),
            timestamp=row["timestamp"]
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to save trajectory")

@router.get("/trajectory/{traj_id}", response_model=TrajectoryInDB)
def get_trajectory(traj_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trajectories WHERE id = ?", (traj_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return TrajectoryInDB(
            id=row["id"],
            wall={"width": row["wall_width"], "height": row["wall_height"]},
            obstacles=json.loads(row["obstacles"]),
            path=json.loads(row["trajectory"]),
            timestamp=row["timestamp"]
        )
    else:
        raise HTTPException(status_code=404, detail="Trajectory not found")

@router.get("/trajectories", response_model=List[TrajectoryInDB])
def list_trajectories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trajectories ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append(TrajectoryInDB(
            id=row["id"],
            wall={"width": row["wall_width"], "height": row["wall_height"]},
            obstacles=json.loads(row["obstacles"]),
            path=json.loads(row["trajectory"]),
            timestamp=row["timestamp"]
        ))
    return result
