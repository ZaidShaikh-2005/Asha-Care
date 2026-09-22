import os
import sys
import threading
import time
import socket


# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    APP_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = BASE_DIR

sys.path.insert(0, BASE_DIR)

os.chdir(APP_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)


# --------------------------------------------------
# START DJANGO USING WAITRESS
# --------------------------------------------------

def run_server():
    try:
        from config.wsgi import application
        from waitress import serve

        serve(
            application,
            host="127.0.0.1",
            port=8000,
            threads=4
        )

    except Exception:
        import traceback

        error = traceback.format_exc()

        error_file = os.path.join(
            APP_DIR,
            "asha_error.log"
        )

        with open(
            error_file,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(error)


# --------------------------------------------------
# WAIT UNTIL SERVER IS READY
# --------------------------------------------------

def wait_for_server(timeout=30):

    start = time.time()

    while time.time() - start < timeout:

        try:
            with socket.create_connection(
                ("127.0.0.1", 8000),
                timeout=1
            ):
                return True

        except OSError:
            time.sleep(0.25)

    return False


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    server_thread = threading.Thread(
        target=run_server,
        daemon=True
    )

    server_thread.start()

    if not wait_for_server():

        import ctypes

        ctypes.windll.user32.MessageBoxW(
            0,
            "ASHA Care could not start.\n\n"
            "Please check asha_error.log.",
            "ASHA Care",
            0x10
        )

        sys.exit(1)

    import webview

    webview.create_window(
        "ASHA Care",
        "http://127.0.0.1:8000/",
        width=1280,
        height=800,
        min_size=(1000, 650),
        resizable=True
    )

    webview.start()