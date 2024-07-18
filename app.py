from flask import Flask

from extensions import api, db, jwt, cors
from api import ns1, ns2, ns3, ns4, ns5, aut
from db_models import Ugyfel

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["JWT_SECRET_KEY"] = "almafa"
    api.init_app(app,
                 title="REST API",
                 description="Banki ugyfelek szamlainak kezelesere szolgalo api (flask-restx)",
                 version="1.0")
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    api.add_namespace(ns1)
    api.add_namespace(ns2)
    api.add_namespace(ns3)
    api.add_namespace(ns4)
    api.add_namespace(ns5)
    api.add_namespace(aut)

    @jwt.user_identity_loader
    def user_identity_lookup(ugyfel):
        return ugyfel.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Ugyfel.query.filter_by(id=identity).first()

    return app


'''
A program virtulis környezetben kerül meghívásra:
Flask run - autómatikusan mehívja az app.py elnevezésű fájlt
'''