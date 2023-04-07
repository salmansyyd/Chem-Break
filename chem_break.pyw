import webbrowser
from app import create_app
from config import Production


app = create_app(config=Production)
url = "http://localhost:5000/"

if __name__ == '__main__':
    webbrowser.open(url)
    app.run()
