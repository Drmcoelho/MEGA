from __future__ import annotations
import json, time, sqlite3, threading
from pathlib import Path
from typing import Dict, Tuple, List
from mega_common.logging import get_logger

log = get_logger("adaptive.storage")


class JSONStorage:
    def __init__(self, path: Path):
        self.path = path
        self._data = {"intervals": {}, "mastery": {}}
        self._loaded = False
        self._lock = threading.RLock()

    def load(self):
        with self._lock:
            if self._loaded:
                return
            if self.path.exists():
                try:
                    self._data = json.loads(self.path.read_text(encoding="utf-8"))
                except Exception as e:
                    log.warning("Falha ao carregar JSONStorage: %s", e)
            self._loaded = True

    def save(self):
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(
                json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            tmp.replace(self.path)

    def get_interval(self, item_id: str) -> Tuple[int, int]:
        self.load()
        return tuple(self._data["intervals"].get(item_id, [0, 0]))  # type: ignore

    def set_interval(self, item_id: str, interval: int):
        self.load()
        with self._lock:
            self._data["intervals"][item_id] = [interval, int(time.time())]
            self.save()

    def due_items(self) -> List[str]:
        self.load()
        now = int(time.time())
        return [
            k
            for k, (interval, ts) in self._data["intervals"].items()
            if now - ts >= interval
        ]

    def update_mastery(self, subskill: str, rating: int):
        self.load()
        with self._lock:
            score_sum, attempts = self._data["mastery"].get(subskill, [0, 0])
            score_sum += rating
            attempts += 1
            self._data["mastery"][subskill] = [score_sum, attempts]
            self.save()

    def mastery_snapshot(self) -> Dict[str, float]:
        self.load()
        snap = {}
        for s, (score_sum, attempts) in self._data["mastery"].items():
            snap[s] = (
                0.0 if attempts == 0 else round((score_sum / (2 * attempts)) * 100, 2)
            )
        return snap


class SQLiteStorage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._init()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS intervals(
                item_id TEXT PRIMARY KEY,
                interval INTEGER,
                last_ts INTEGER
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS mastery(
                subskill TEXT PRIMARY KEY,
                score_sum INTEGER,
                attempts INTEGER
            )""")

    def get_interval(self, item_id: str):
        with self._conn() as c:
            cur = c.execute(
                "SELECT interval,last_ts FROM intervals WHERE item_id=?", (item_id,)
            )
            row = cur.fetchone()
            return (0, 0) if not row else row

    def set_interval(self, item_id: str, interval: int):
        import time

        ts = int(time.time())
        with self._lock, self._conn() as c:
            c.execute(
                "REPLACE INTO intervals(item_id, interval, last_ts) VALUES(?,?,?)",
                (item_id, interval, ts),
            )

    def due_items(self):
        import time

        now = int(time.time())
        out = []
        with self._conn() as c:
            for item_id, interval, last_ts in c.execute(
                "SELECT item_id, interval, last_ts FROM intervals"
            ):
                if now - last_ts >= interval:
                    out.append(item_id)
        return out

    def update_mastery(self, subskill: str, rating: int):
        with self._lock, self._conn() as c:
            cur = c.execute(
                "SELECT score_sum, attempts FROM mastery WHERE subskill=?", (subskill,)
            )
            row = cur.fetchone()
            score_sum, attempts = row if row else (0, 0)
            score_sum += rating
            attempts += 1
            c.execute(
                "REPLACE INTO mastery(subskill,score_sum,attempts) VALUES(?,?,?)",
                (subskill, score_sum, attempts),
            )

    def mastery_snapshot(self):
        snap = {}
        with self._conn() as c:
            for subskill, score_sum, attempts in c.execute(
                "SELECT subskill,score_sum,attempts FROM mastery"
            ):
                snap[subskill] = (
                    0.0
                    if attempts == 0
                    else round((score_sum / (2 * attempts)) * 100, 2)
                )
        return snap
