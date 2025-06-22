# Autonomous Wall-Finishing Robot Control System

## Overview
This project is a backend and frontend system designed to control an autonomous wall-finishing robot. It includes:

- **Coverage Planning:** Calculates a path for the robot to cover a rectangular wall while avoiding rectangular obstacles.
- **Backend API:** Built with FastAPI, it provides endpoints to plan, save, and retrieve robot trajectories.
- **Database:** Uses SQLite to store trajectory data with basic indexing for efficient queries.
- **Frontend Visualization:** A simple web page that visualizes the robot's trajectory in 2D using HTML Canvas.
- **Logging:** Logs all API requests and response times for monitoring.
- **Testing:** Automated tests to verify API functionality and performance.

---

## Project Structure

```
wall_robot/
│
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Data models for request/response validation
│   ├── db.py                # SQLite database connection and schema setup
│   ├── routes.py            # API route handlers (plan, save, retrieve trajectories)
│   ├── coverage.py          # Coverage planning logic (currently placeholder)
│   ├── logger.py            # Logging setup and middleware for request timing
│   └── utils.py             # Utility functions (optional)
│
├── static/
│   └── index.html           # Frontend visualization using HTML Canvas
│
├── tests/
│   └── test_api.py          # Pytest tests for API endpoints
│
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Setup Instructions

1. **Create and activate a Python virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install required packages:**

```bash
pip install -r requirements.txt
```

3. **Run the FastAPI server:**

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

4. **Open the frontend visualization:**

Open the file `wall_robot/static/index.html` in your web browser (e.g., drag and drop or use `file://` URL).

---

## API Usage

### 1. Plan a Trajectory

- **Endpoint:** `POST /plan`
- **Description:** Submit wall dimensions and obstacles to receive a planned trajectory path.
- **Request Body Example:**

```json
{
  "wall": {"width": 5.0, "height": 5.0},
  "obstacles": [
    {"x": 1.0, "y": 1.0, "width": 0.25, "height": 0.25}
  ]
}
```

- **Response:** List of (x, y) points representing the robot's path.

### 2. Save a Trajectory

- **Endpoint:** `POST /trajectory`
- **Description:** Save a planned trajectory to the database.
- **Request Body:** Includes wall, obstacles, and path (list of points).

### 3. Retrieve a Trajectory by ID

- **Endpoint:** `GET /trajectory/{id}`
- **Description:** Fetch a saved trajectory by its unique ID.

### 4. List All Trajectories

- **Endpoint:** `GET /trajectories`
- **Description:** Retrieve all saved trajectories, ordered by timestamp.

---

## Frontend Visualization

- The visualization uses an HTML Canvas to draw the robot's trajectory.
- Playback controls allow you to play, pause, and reset the animation of the robot moving along the path.
- By default, it fetches trajectory with ID 1 from the backend API. Update the ID in `index.html` as needed.


## Overview

<img width="1440" alt="Screenshot 2025-06-19 at 17 41 53" src="https://github.com/user-attachments/assets/b7244226-bab7-49d9-9b83-ce9365817bf9" />



<img width="1440" alt="Screenshot 2025-06-19 at 17 42 06" src="https://github.com/user-attachments/assets/0a60c569-49c2-4ffb-ae2b-19571f95680c" />

---

## Testing

- Run automated tests using pytest:

```bash
pytest
```

- Tests cover API endpoints for planning, saving, retrieving, and listing trajectories.

---

## Logging

- All API requests and their response times are logged to the console.
- Logging is implemented as FastAPI middleware in `app/logger.py`.

---

## Notes

- The current coverage planning logic is a simple zig-zag pattern and does not yet avoid obstacles.
- The project is designed to be extensible for more advanced path planning and real-time communication features.

---

If you have any questions or need assistance, please feel free to ask.
