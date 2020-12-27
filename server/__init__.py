from flask import Flask



def create_app():
    #Create app
    app = Flask(__name__)
    
    
    #Intialize modules
    from server.api.routes import api
    app.register_blueprint(api, url_prefix="/api/v1")
    return app