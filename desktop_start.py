import webview
import sys
import threading

from app import create_app
from config import Config

app = create_app(config=Config)


def start_server():
    app.run()


if __name__ == '__main__':

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("ChemBreak", "http://localhost:5000")
    webview.start()
    sys.exit()
