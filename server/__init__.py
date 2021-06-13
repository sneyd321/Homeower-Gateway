from flask import Flask, Response
from kazoo.client import KazooClient, KazooState

zk = KazooClient(hosts='host.docker.internal:2181')
zk.start()


app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>Homeowner Gateway!!!</h1>"

@app.route("/Health")
def health_check():
    return Response(status=200)

@app.route("/favicon.ico")
def favicon():
    return Response(status=200)


def create_app():
    #Create app
    global app
    #Intialize modules
    from server.api.routes import api
    app.register_blueprint(api, url_prefix="/homeowner-gateway/v1")
    return app