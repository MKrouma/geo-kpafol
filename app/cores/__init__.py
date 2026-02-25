from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
cors = CORS()
bootstrap = Bootstrap()
login = LoginManager()