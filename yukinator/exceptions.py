class WrongQueryParameters(Exception):
    """Raised when the expected output for a given parameters is empty."""

    def __str__(self):
        return "The output for provided query parameters is empty."


class WrongDirectory(Exception):
    """Raised when the directory for cache does not exist."""

    def __str__(self):
        return "The provider directory for a cache does not exist."
