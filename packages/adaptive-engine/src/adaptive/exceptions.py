class AdaptiveError(Exception):
    """Base para erros do motor adaptativo."""

class InvalidRatingError(AdaptiveError):
    pass

class BackendNotSupportedError(AdaptiveError):
    pass