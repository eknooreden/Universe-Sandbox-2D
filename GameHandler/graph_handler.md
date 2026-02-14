# 📈 Graph & Run Data Backend Handling

This page documents the **graphing + data logging backend** used to track how many celestial bodies exist over time during a run, save that run to JSON, and optionally display a graph.

File Path: `UniverseSandbox2D/GameHandler/graph_handler.py`

---

## What this file does

This module is responsible for:

- Tracking body count over time (sampled every N seconds)
- Displaying a graph of bodies vs time
- Saving each run into a persistent JSON log

---

## Imports

`GameHandler/graph_handler.py`

```python
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
```

- **json / os** → file handling  
- **datetime** → timestamps  
- **matplotlib** → graph rendering

---

## RunTracker Class

Tracks points like:

```json
{"t": 30.0, "bodies": 5}
```

```python
class RunTracker:
    """
    Tracks body count over time (sampled every N seconds).
    """

    def __init__(self, sample_every_seconds=30.0):
        self.sample_every = float(sample_every_seconds)
        self.points = []
        self._t = 0.0
        self._since_sample = 0.0

    def update(self, dt, body_count):
        self._t += dt
        self._since_sample += dt

        while self._since_sample >= self.sample_every:
            self._since_sample -= self.sample_every
            t_mark = self._t - self._since_sample

            self.points.append({
                "t": round(t_mark, 3),
                "bodies": int(body_count)
            })

    def time_ended_seconds(self):
        return round(self._t, 3)

    def body_points(self):
        return self.points
```

---

## Example Usage

`UniverseSandbox2D/main.py`

```python
tracker = RunTracker(sample_every_seconds=10.0)
tracker.update(dt, len(bodies))
```

---

## Example JSON Output

`UniverseSandbox2D/game_data.json`

```json
[
  {
    "body_points": [
      { "t": 30.0, "bodies": 10 },
      { "t": 60.0, "bodies": 6 },
      { "t": 90.0, "bodies": 21 }
    ],
    "time_ended": 111.71,
    "date_done": "2026-02-13T15:48:08-08:00"
  }
]
```

---

## Graph Display

```python
def show_graph(self, title="Bodies Over Time"):
    if not self.points:
        print("[graph_handler] No points collected yet.")
        return

    xs = [p["t"] for p in self.points]
    ys = [p["bodies"] for p in self.points]

    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bodies")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```

---

## JSON Helpers

```python
def _read_json_list(path):
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return []
            data = json.loads(raw)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []
```

```python
def append_run_to_json(json_path, body_points, time_ended, date_done):
    runs = _read_json_list(json_path)

    runs.append({
        "body_points": body_points,
        "time_ended": time_ended,
        "date_done": date_done
    })

    folder = os.path.dirname(json_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(runs, f, indent=2)
```

---

🚀 End of Graph Backend Documentation