from app import create_app, db
from flask_migrate import Migrate

# Initialize the application using the factory function
app = create_app()

# Set up Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

if __name__ == '__main__':
    # Start the Flask application with debug mode enabled
    app.run(debug=True)