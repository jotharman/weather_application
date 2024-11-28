from flask import Blueprint, request, jsonify
from app.models import WeatherData, WeatherStats
from flask_restx import Api, Resource, fields
from app import db

# Blueprint for API
api_blueprint = Blueprint('api', __name__)

# Initialize the API
api = Api(
    api_blueprint,
    version='1.0',
    title='Weather API',
    description='API for managing and retrieving weather data and statistics'
)

# Define the model for weather data
weather_data_model = api.model('WeatherData', {
    'station_id': fields.String(required=True, description='Weather station ID'),
    'date': fields.String(required=True, description='Date of the weather data (YYYY-MM-DD)'),
    'max_temp': fields.Float(description='Maximum temperature in Celsius'),
    'min_temp': fields.Float(description='Minimum temperature in Celsius'),
    'precipitation': fields.Float(description='Precipitation in mm')
})

# Define the model for weather statistics
weather_stats_model = api.model('WeatherStats', {
    'station_id': fields.String(required=True, description='Weather station ID'),
    'year': fields.Integer(required=True, description='Year of the statistics'),
    'avg_max_temp': fields.Float(description='Average maximum temperature in Celsius'),
    'avg_min_temp': fields.Float(description='Average minimum temperature in Celsius'),
    'total_precipitation': fields.Float(description='Total precipitation in mm')
})

# Route to retrieve weather data
@api.route('/api/weather')
@api.param('station_id', 'Weather station ID (optional)', type=str)
@api.param('date', 'Date of the weather data (optional, YYYY-MM-DD)', type=str)
class WeatherDataResource(Resource):
    def get(self):
        """
        Retrieve weather data.
        Filters:
        - `station_id` (optional): Filter by weather station ID.
        - `date` (optional): Filter by specific date in the format YYYY-MM-DD.

        Pagination:
        - Default page size is 10 records.
        """
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        query = WeatherData.query

        # Apply filters
        if station_id:
            query = query.filter_by(station_id=station_id)
        if date:
            query = query.filter_by(date=date)

        # Apply pagination
        results = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)

        # Return results in a structured format
        return [{
            'station_id': data.station_id,
            'date': data.date.isoformat(),
            'max_temp': data.max_temp,
            'min_temp': data.min_temp,
            'precipitation': data.precipitation
        } for data in results.items]


# Route to retrieve weather statistics
@api.route('/api/weather/stats')
@api.param('station_id', 'Weather station ID (optional)', type=str)
@api.param('year', 'Year of the weather stats (optional)', type=int)
class WeatherStatsResource(Resource):
    def get(self):
        """
        Retrieve weather statistics.
        Filters:
        - `station_id` (optional): Filter by weather station ID.
        - `year` (optional): Filter by specific year.

        Pagination:
        - Default page size is 10 records.
        """
        station_id = request.args.get('station_id')
        year = request.args.get('year')
        query = WeatherStats.query

        # Apply filters
        if station_id:
            query = query.filter_by(station_id=station_id)
        if year:
            query = query.filter_by(year=int(year))

        # Apply pagination
        results = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)

        # Return results in a structured format
        return [{
            'station_id': stat.station_id,
            'year': stat.year,
            'avg_max_temp': stat.avg_max_temp,
            'avg_min_temp': stat.avg_min_temp,
            'total_precipitation': stat.total_precipitation
        } for stat in results.items]