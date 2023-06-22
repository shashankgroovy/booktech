"""Launch the main celery app"""

from booktech.app import app


if __name__ == '__main__':
    app.start()

