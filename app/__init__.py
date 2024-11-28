from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app(config_name='development'):
    """
    Factory function to create and configure the Flask application.

    Args:
        config_name (str): Configuration name to determine the app's environment. 
                           Defaults to 'development'.

    Returns:
        Flask app: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Configuration mapping for different environments
    config_mapping = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig'
    }

    # Load configuration based on the provided environment
    app.config.from_object(config_mapping.get(config_name, 'config.Config'))

    # Initialize the database with the app instance
    db.init_app(app)

    # Perform actions within the app context
    with app.app_context():
        # Import models and utility functions
        from .models import WeatherData  # Weather data table definition
        from .ingestion import ingest_weather_data  # Function to ingest weather data
        from .analysis import calculate_weather_stats  # Function to calculate weather statistics

        # Create all database tables defined in the models
        db.create_all()

        # Verify database connection
        try:
            # Use `db.engine` to get the SQLAlchemy engine
            connection = db.engine.connect()
            
            # Execute a simple query to test the database connection
            result = connection.execute(text("SELECT 1")).scalar()  # Should return 1 if successful
            connection.close()  # Ensure the connection is closed after the test

            if result == 1:
                print("Database connection successful!")
            else:
                print("Database connection failed!")
        except Exception as e:
            print(f"Database connection failed: {e}")

        # Add custom objects to the Flask shell context
        @app.shell_context_processor
        def make_shell_context():
            """
            Add objects to the Flask shell for easier access when debugging.

            Returns:
                dict: Mappings of names to objects for use in the Flask shell.
            """
            return {
                'db': db,
                'WeatherData': WeatherData,
                'ingest_weather_data': ingest_weather_data,
                'calculate_weather_stats': calculate_weather_stats
            }

    # Register API routes as a Flask blueprint
    from .routes import api_blueprint  # Assuming you have defined API routes in `routes.py`
    app.register_blueprint(api_blueprint)

    # Return the configured Flask app instance
    return app