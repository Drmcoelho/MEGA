class MasteryTracker:
    """
    Mastery por subskill: média ponderada incremental.
    rating: 0 erro, 1 parcial, 2 correto.
    """
    def __init__(self):
        self._stats = {}  # subskill -> (score_sum, attempts)

    def update(self, subskill: str, rating: int):
        score_sum, attempts = self._stats.get(subskill, (0, 0))
        score_sum += rating
        attempts += 1
        self._stats[subskill] = (score_sum, attempts)

    def mastery(self, subskill: str) -> float:
        score_sum, attempts = self._stats.get(subskill, (0, 0))
        if attempts == 0:
            return 0.0
        return round((score_sum / (2 * attempts)) * 100, 2)  # percent

    def snapshot(self):
        return {s: self.mastery(s) for s in self._stats}