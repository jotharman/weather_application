import pytest
from app import create_app, db
from app.models import WeatherData
import os

@pytest.fixture(scope='function')
def app():
    """Fixture to create and configure the Flask application for testing."""
    app = create_app('testing')  # Ensure 'testing' is a valid configuration
    with app.app_context():
        db.drop_all()  # Drop all tables before each test
        db.create_all()  # Recreate tables before each test
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_data_ingestion(client, app):
    # Insert some data manually
    with app.app_context():
        data_file = os.path.join(os.path.dirname(__file__), 'test_data.txt')
        print(data_file)
        # Run your data ingestion function
        from app.ingestion import ingest_weather_data
        ingest_weather_data(data_file)

    # Query the database to check if the data was ingested
    
        data = WeatherData.query.filter_by(station_id="test_data", date="2022-11-01").first()
        print(data)
        assert data is not None
        assert data.max_temp == 25.0  # assuming max_temp was divided by 10 during ingestion

def test_duplicate_data(client, app):
    # Test that duplicate data does not get inserted
    from app.ingestion import ingest_weather_data
    with app.app_context():
        data_file = os.path.join(os.path.dirname(__file__), 'test_data.txt')
        ingest_weather_data(data_file)
        # Count how many records exist for the same date and station
        data_count = WeatherData.query.filter_by(station_id="test_data", date="2022-11-01").count()
        assert data_count == 1  # Ensure only one record exists
