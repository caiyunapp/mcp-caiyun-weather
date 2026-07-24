from ._version import __version__
from . import server


def main():
    """Main entry point for the package."""
    server.main()


# Optionally expose other important items at package level
__all__ = ["main", "server", "__version__"]
