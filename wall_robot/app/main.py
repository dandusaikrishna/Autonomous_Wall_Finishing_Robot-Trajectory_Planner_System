from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Adjust sys.path to include the app directory for imports
sys.path.append(os.path.dirname(__file__))

from routes import router
from logger import setup_logging
import uvicorn

app = FastAPI()

# Setup logging
setup_logging(app)

# Include API routes
app.include_router(router)

# Mount static files directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "..", "static", "index.html"))

if __name__ == "__main__":
    uvicorn.run("wall_robot.app.main:app", host="0.0.0.0", port=8000, reload=True)
