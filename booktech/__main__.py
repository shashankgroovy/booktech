"""Launch the main celery app"""

from booktech.celery import app


if __name__ == '__main__':
    app.start()

