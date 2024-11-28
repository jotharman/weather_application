from app import db

class WeatherData(db.Model):
    """
    Represents the daily weather data for a station.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for each record.
        station_id (str): Identifier for the weather station.
        date (Date): The date of the weather record.
        max_temp (float, optional): Maximum temperature recorded on the date (in degrees Celsius).
        min_temp (float, optional): Minimum temperature recorded on the date (in degrees Celsius).
        precipitation (float, optional): Total precipitation recorded on the date (in mm).

    Constraints:
        - A unique combination of `station_id` and `date` ensures no duplicate records for the same station and date.
    """
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Float, nullable=True)
    min_temp = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)

    # Ensure unique combination of station_id and date
    __table_args__ = (
        db.UniqueConstraint('station_id', 'date', name='uix_station_date'),
    )


class WeatherStats(db.Model):
    """
    Represents aggregated yearly weather statistics for a station.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for each record.
        station_id (str): Identifier for the weather station.
        year (int): The year of the aggregated statistics.
        avg_max_temp (float, optional): Average of maximum daily temperatures for the year.
        avg_min_temp (float, optional): Average of minimum daily temperatures for the year.
        total_precipitation (float, optional): Total precipitation recorded for the year (in mm).
    """
    __tablename__ = 'weather_stats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_precipitation = db.Column(db.Float, nullable=True)