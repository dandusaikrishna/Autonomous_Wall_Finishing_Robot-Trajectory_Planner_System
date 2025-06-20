from pydantic import BaseModel, Field
from typing import List

class Wall(BaseModel):
    width: float = Field(..., description="Width of the wall in meters")
    height: float = Field(..., description="Height of the wall in meters")

class Obstacle(BaseModel):
    x: float = Field(..., description="X coordinate of the obstacle's bottom-left corner in meters")
    y: float = Field(..., description="Y coordinate of the obstacle's bottom-left corner in meters")
    width: float = Field(..., description="Width of the obstacle in meters")
    height: float = Field(..., description="Height of the obstacle in meters")

class TrajectoryPoint(BaseModel):
    x: float = Field(..., description="X coordinate of the trajectory point in meters")
    y: float = Field(..., description="Y coordinate of the trajectory point in meters")

class PlanInput(BaseModel):
    wall: Wall
    obstacles: List[Obstacle]

class TrajectoryCreate(BaseModel):
    wall: Wall
    obstacles: List[Obstacle]
    path: List[TrajectoryPoint]

class TrajectoryInDB(TrajectoryCreate):
    id: int
    timestamp: str
