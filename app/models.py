from app import db

class WeatherData(db.Model):
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
    __tablename__ = 'weather_stats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_precipitation = db.Column(db.Float, nullable=True)
