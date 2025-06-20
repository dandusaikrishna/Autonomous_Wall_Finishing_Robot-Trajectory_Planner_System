# Wall Finishing Robot Trajectory Planner - Run Instructions

## Prerequisites
- Python 3.9+
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```
`ˀˀˀˀˀ
3. Initialize the SQLite database:ˀ

```bash`ˀ
python -c "from app.db import init_db; init_db()"
```

## Running the Backend Server

Start the FastAPI server with:

```bash
uvicorn wall_robot.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## Running Tests

Run backend API tests with:

```bash
pytest wall_robot/tests/test_api.py --disable-warnings -v
```

## Accessing the Frontend

Open your browser and navigate to:

```
http://localhost:8000
```

Use the web interface to input wall dimensions, obstacles, and plan trajectories. Playback controls are available below the visualization.

## Notes

- The backend logs all requests and response times.
- The frontend uses HTML Canvas for 2D visualization.
- The database file `wall_robot.db` is created in the project root.

For any issues, please check the console logs for errors.
