import pytest
from datetime import datetime
from app import create_app, db
from app.models import WeatherData

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
    """Fixture to create a test client for the app."""
    return app.test_client()

def test_get_weather_data(client, app):
    """Test the /api/weather endpoint."""
    with app.app_context():
        # Add unique weather data
        data = WeatherData(
            station_id="test_station",
            date=datetime.strptime("2022-11-01", "%Y-%m-%d").date(),
            max_temp=25.0,
            min_temp=20.0,
            precipitation=100.0
        )
        db.session.add(data)
        db.session.commit()

    # Test the endpoint
    response = client.get('/api/weather?station_id=test_station&date=2022-11-01')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json[0]['station_id'] == 'test_station'
    assert response_json[0]['date'] == '2022-11-01'
    assert response_json[0]['max_temp'] == 25.0

def test_get_weather_stats(client, app):
    """Test the /api/weather/stats endpoint."""
    with app.app_context():
        # Add unique weather data
        data = WeatherData(
            station_id="test_station",
            date=datetime.strptime("2022-11-01", "%Y-%m-%d").date(),
            max_temp=25.0,
            min_temp=20.0,
            precipitation=100.0
        )
        db.session.add(data)
        db.session.commit()

        # Run stats calculation (make sure this function exists in your app)
        from app.analysis import calculate_weather_stats
        calculate_weather_stats()

    # Test the endpoint
    response = client.get('/api/weather/stats?station_id=test_station&year=2022')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json[0]['station_id'] == 'test_station'
    assert response_json[0]['year'] == 2022
    assert response_json[0]['avg_max_temp'] == 25.0
    assert response_json[0]['avg_min_temp'] == 20.0