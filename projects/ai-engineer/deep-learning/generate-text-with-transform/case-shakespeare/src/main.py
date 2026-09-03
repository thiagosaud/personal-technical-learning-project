"""Compatibility entrypoint for the reorganized Shakespeare app structure."""

# Import the CLI entry function so the package can be executed with a standard Python module invocation.
from src.app.cli import main

# Execute the CLI when this module is launched directly.
if __name__ == "__main__":
    main()
