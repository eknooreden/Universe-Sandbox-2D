import json
import os
from datetime import datetime

import matplotlib.pyplot as plt


def now_iso():
    # Example: 2026-02-13T13:05:22-08:00
    return datetime.now().astimezone().isoformat(timespec="seconds")


class RunTracker:
    """
    Tracks body count over time (sampled every N seconds).
    Stores points like: {"t": 30.0, "bodies": 5}
    """

    def __init__(self, sample_every_seconds=30.0):
        self.sample_every = float(sample_every_seconds)
        self.points = []  # list[dict]: {"t": float, "bodies": int}
        self._t = 0.0
        self._since_sample = 0.0

    def update(self, dt, body_count):
        """
        Call once per frame.
        dt: seconds since last frame
        body_count: len(bodies)
        """
        self._t += dt
        self._since_sample += dt

        # If a lag spike happens, we may need to record multiple intervals
        while self._since_sample >= self.sample_every:
            self._since_sample -= self.sample_every

            # Timestamp close to the exact sample mark
            t_mark = self._t - self._since_sample

            self.points.append({
                "t": round(t_mark, 3),
                "bodies": int(body_count)
            })

    def time_ended_seconds(self):
        return round(self._t, 3)

    def body_points(self):
        return self.points

    def show_graph(self, title="Bodies Over Time"):
        if not self.points:
            print("[graph_handler] No points collected yet (run longer than 30s to see samples).")
            return

        xs = [p["t"] for p in self.points]
        ys = [p["bodies"] for p in self.points]

        plt.figure()
        plt.plot(xs, ys, '-')
        plt.title(title)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Bodies")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def _read_json_list(path):
    """
    Returns a list. If file doesn't exist or is invalid, returns [].
    """
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


def append_run_to_json(json_path, body_points, time_ended, date_done):
    """
    Appends one run record to json_path.
    File format: a JSON LIST of run objects.
    """
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

    print(f"[graph_handler] Saved run to: {os.path.abspath(json_path)}")