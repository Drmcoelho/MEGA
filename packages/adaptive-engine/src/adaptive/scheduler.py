from __future__ import annotations
from dataclasses import dataclass
from .exceptions import InvalidRatingError
from mega_common.config import CONFIG

@dataclass
class IntervalResult:
    item_id: str
    rating: int
    previous_interval: int
    next_interval: int

class IntervalScheduler:
    """Cálculo de intervalos com fatores de crescimento configuráveis."""

    def __init__(self, *, min_interval: int | None = None, medium: int | None = None, long: int | None = None,
                 growth_partial: float | None = None, growth_correct: float | None = None):
        a = CONFIG.adaptive
        self.min_interval = min_interval or a.min_interval_seconds
        self.med_interval = medium or a.medium_interval_seconds
        self.long_interval = long or a.long_interval_seconds
        self.growth_partial = growth_partial or a.growth_factor_partial
        self.growth_correct = growth_correct or a.growth_factor_correct

    def compute_interval(self, last_interval: int, rating: int) -> int:
        if rating not in (0,1,2):
            raise InvalidRatingError(f"Rating inválido: {rating}")
        if rating == 0:
            return self.min_interval
        if rating == 1:
            base = int(last_interval * self.growth_partial) if last_interval else self.med_interval
            return max(self.med_interval, base)
        base = int(last_interval * self.growth_correct) if last_interval else self.long_interval
        return max(self.long_interval, base)

    def next(self, item_id: str, last_interval: int, rating: int) -> IntervalResult:
        nxt = self.compute_interval(last_interval, rating)
        return IntervalResult(item_id=item_id, rating=rating, previous_interval=last_interval, next_interval=nxt)