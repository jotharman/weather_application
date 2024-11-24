import pytest
from app import create_app, db
from app.models import WeatherData, WeatherStats
from app.analysis import calculate_weather_stats
from datetime import datetime

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

def test_weather_stats_calculation(client, app):
    # Add weather data manually to the database
    with app.app_context():  # Ensure this block runs within app context
        # Ensure we pass a datetime.date object, not a string
        date_1 = datetime.strptime("2022-11-01", '%Y-%m-%d').date()
        date_2 = datetime.strptime("2022-11-02", '%Y-%m-%d').date()

        # Add the data
        data_1 = WeatherData(station_id="test_station", date=date_1, max_temp=25.0, min_temp=20.0, precipitation=100.0)
        db.session.add(data_1)
        db.session.commit()  # Commit the first record

        data_2 = WeatherData(station_id="test_station", date=date_2, max_temp=None, min_temp=18.0, precipitation=None)
        db.session.add(data_2)
        db.session.commit()  # Commit the second record

        # Now, calculate stats
        calculate_weather_stats()

        # Check if stats are correctly calculated
        stats = WeatherStats.query.filter_by(station_id="test_station", year=2022).first()

        # Assert the stats exist and have the correct values
        assert stats is not None
        assert stats.avg_max_temp == 25.0  # Ignoring the None value
        assert stats.avg_min_temp == 19.0  # (20 + 18) / 2
        assert stats.total_precipitation == 100.0
