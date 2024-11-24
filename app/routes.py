from flask import Blueprint, request, jsonify
from app.models import WeatherData, WeatherStats
from flask_restx import Api, Resource, fields
from app import db

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint, version='1.0', title='Weather API', description='API for weather data and stats')



weather_data_model = api.model('WeatherData', {
    'station_id': fields.String(required=True, description='Weather station ID'),
    'date': fields.String(required=True, description='Date of the weather data'),
    'max_temp': fields.Float(description='Maximum temperature'),
    'min_temp': fields.Float(description='Minimum temperature'),
    'precipitation': fields.Float(description='Precipitation in mm')
})

# Define the model for weather stats
weather_stats_model = api.model('WeatherStats', {
    'station_id': fields.String(required=True, description='Weather station ID'),
    'year': fields.Integer(required=True, description='Year of the stats'),
    'avg_max_temp': fields.Float(description='Average maximum temperature'),
    'avg_min_temp': fields.Float(description='Average minimum temperature'),
    'total_precipitation': fields.Float(description='Total precipitation')
})

# Route to get weather data
@api.route('/api/weather')
@api.param('station_id', 'Weather station ID (optional)', type=str)
@api.param('date', 'Date of the weather data (optional)', type=str)
class WeatherDataResource(Resource):
    def get(self):
        """Get weather data"""
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        query = WeatherData.query

        if station_id:
            query = query.filter_by(station_id=station_id)
        if date:
            query = query.filter_by(date=date)

        results = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
        return [{
            'station_id': data.station_id,
            'date': data.date.isoformat(),
            'max_temp': data.max_temp,
            'min_temp': data.min_temp,
            'precipitation': data.precipitation
        } for data in results.items]


# Route to get weather stats
@api.route('/api/weather/stats')
@api.param('station_id', 'Weather station ID (optional)', type=str)
@api.param('year', 'Year of the weather stats (optional)', type=int)
class WeatherStatsResource(Resource):
    def get(self):
        """Get weather stats"""
        station_id = request.args.get('station_id')
        year = request.args.get('year')
        query = WeatherStats.query

        if station_id:
            query = query.filter_by(station_id=station_id)
        if year:
            query = query.filter_by(year=int(year))

        results = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
        return [{
            'station_id': stat.station_id,
            'year': stat.year,
            'avg_max_temp': stat.avg_max_temp,
            'avg_min_temp': stat.avg_min_temp,
            'total_precipitation': stat.total_precipitation
        } for stat in results.items]