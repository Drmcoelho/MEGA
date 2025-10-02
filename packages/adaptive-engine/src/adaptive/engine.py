from __future__ import annotations
from pathlib import Path
from .storage import JSONStorage, SQLiteStorage
from .scheduler import IntervalScheduler
from .exceptions import BackendNotSupportedError, InvalidRatingError
from mega_common.config import CONFIG
from mega_common.logging import get_logger
from dataclasses import asdict

log = get_logger("adaptive.engine")

class AdaptiveEngine:
    def __init__(self, backend: str | None = None, path: str | None = None):
        a = CONFIG.adaptive
        self.backend = backend or a.backend
        data_path = path or a.path
        p = Path(data_path)
        if self.backend == "json":
            self.store = JSONStorage(p)
        elif self.backend == "sqlite":
            self.store = SQLiteStorage(p)
        else:
            raise BackendNotSupportedError(self.backend)
        self.scheduler = IntervalScheduler()

    def rate_item(self, item_id: str, rating: int):
        if rating not in (0,1,2):
            raise InvalidRatingError(rating)
        last_interval,_ = self.store.get_interval(item_id)
        result = self.scheduler.next(item_id, last_interval, rating)
        self.store.set_interval(item_id, result.next_interval)
        log.debug("Rated item %s => %s", item_id, asdict(result))
        return result

    def update_mastery(self, subskill: str, rating: int):
        if rating not in (0,1,2):
            raise InvalidRatingError(rating)
        self.store.update_mastery(subskill, rating)
        snap = self.store.mastery_snapshot()
        return {"subskill": subskill, "mastery": snap.get(subskill, 0.0)}

    def due(self):
        return self.store.due_items()

    def snapshot(self):
        return self.store.mastery_snapshot()