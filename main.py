from server import create_app
import os


ENV = os.getenv('ENV')

app = create_app(ENV)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)