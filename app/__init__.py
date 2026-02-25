from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from .config.config import config_dict
from .main.views import main
from .auth.views import auth
from .cores import db, migrate, bootstrap, login
from .models.users import User

def create_app(config_name='default'): 

    #flask app
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # instanciation
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    
    # Configure Flask-Login
    login.init_app(app)
    # login.login_view = 'auth.login'
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # # Register commands
    # app.cli.add_command(clean_villages)
    # app.cli.add_command(clean_villages_lulc)
    
    return app