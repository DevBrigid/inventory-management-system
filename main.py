#Inventory app entrypoint.

from routes import app


def create_app():
    return app


if __name__ == "__main__":
    create_app().run(port=5555, debug=True)
