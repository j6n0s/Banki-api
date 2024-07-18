from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

cors = CORS()
api = Api()
db = SQLAlchemy()
jwt = JWTManager()
