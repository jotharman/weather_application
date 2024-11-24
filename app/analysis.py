from sqlalchemy.sql import func
from app import db
from app.models import WeatherData, WeatherStats

def calculate_weather_stats():
    # Query to calculate average temperature and total precipitation for each station by year
    stats = db.session.query(
        WeatherData.station_id,
        func.extract('year', WeatherData.date).label('year'),
        func.avg(WeatherData.max_temp).label('avg_max_temp'),
        func.avg(WeatherData.min_temp).label('avg_min_temp'),
        func.sum(WeatherData.precipitation).label('total_precipitation')
    ).group_by(WeatherData.station_id, func.extract('year', WeatherData.date)).all()

    # Iterate over the calculated statistics
    for station_id, year, avg_max, avg_min, total_precip in stats:
        # Ensure that we only store records where there is valid data
        stat = WeatherStats(
            station_id=station_id,
            year=year,
            avg_max_temp=avg_max if avg_max is not None else None,
            avg_min_temp=avg_min if avg_min is not None else None,
            total_precipitation=total_precip if total_precip is not None else None
        )
        db.session.merge(stat)  # Merge to prevent duplicates
    db.session.commit()
