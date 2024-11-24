from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    config_mapping = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig'
    }
    app.config.from_object(config_mapping.get(config_name, 'config.Config'))
    db.init_app(app)
    

    with app.app_context():
        from .models import WeatherData
        from .ingestion import ingest_weather_data
        from .analysis import calculate_weather_stats
        
        db.create_all()
        try:
            # Use `db.engine` to get the engine object directly
            connection = db.engine.connect()
            
            # Execute a simple query to check the connection
            result = connection.execute(text("SELECT 1")).scalar()  # Returns 1 if connection is successful
            connection.close()  # Don't forget to close the connection after checking
            
            if result == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed!")
                
        except Exception as e:
            print(f"Database connection failed: {e}")
            
        @app.shell_context_processor
        def make_shell_context():
            return {
                'db': db,
                'WeatherData': WeatherData,
                'ingest_weather_data': ingest_weather_data,
                'calculate_weather_stats': calculate_weather_stats
            }
    from .routes import api_blueprint  # Assuming you have an API blueprint
    app.register_blueprint(api_blueprint)
    return app
