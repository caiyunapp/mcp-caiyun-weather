from . import server

__version__ = "0.1.3"


def main():
    """Main entry point for the package."""
    server.main()


# Optionally expose other important items at package level
__all__ = ["main", "server", "__version__"]
