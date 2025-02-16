from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Import the configurations
from instance.config import app_config

database = SQLAlchemy()

def create_app(config_name):
    application = Flask(
        import_name="app",
        template_folder="templates",
        static_folder='static',
        instance_relative_config=True
    )

    application.config.from_object(app_config[config_name])
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(application)
    
    # Setup migrations
    migrate = Migrate(application, database, directory="intron_health_migrations", render_as_batch=True)

    # with application.app_context():  # Ensuring application context is available
    #     from app import models
    #     register_blueprints(application)
    #     database.create_all()

    print("Initializing database...")
    with application.app_context():
        print("Importing models...")
        from app import models
        print("Creating database tables...")
        database.create_all()
        print("Registering blueprints...")
        register_blueprints(application)
        
    print("Database initialized.")
    return application

"""
 The following registers the Blueprints with the application.
"""
def register_blueprints(application):
    from .home import home as home_blueprint
    application.register_blueprint(home_blueprint, url_prefix='/home')


