import os
import sys
import threading
import time
import urllib.request

import webview
from django.core.management import execute_from_command_line


HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}/"


if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))


os.chdir(APP_DIR)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)


def start_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings"
    )

    execute_from_command_line([
        "manage.py",
        "runserver",
        f"{HOST}:{PORT}",
        "--noreload"
    ])


def wait_for_server():

    for _ in range(60):

        try:
            urllib.request.urlopen(
                URL,
                timeout=1
            )

            return True

        except Exception:
            time.sleep(0.25)

    return False


if __name__ == "__main__":

    django_thread = threading.Thread(
        target=start_django,
        daemon=True
    )

    django_thread.start()

    if wait_for_server():

        webview.create_window(
            "Asha Nurse App",
            URL,
            width=1280,
            height=800,
            min_size=(900, 600),
            resizable=True
        )

        webview.start()