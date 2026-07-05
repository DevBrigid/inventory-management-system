# Inventory app entrypoint.

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from routes import app


def create_app():
    return app


if __name__ == "__main__":
    create_app().run(port=5555, debug=True)
