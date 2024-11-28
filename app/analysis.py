from sqlalchemy.sql import func
from app import db
from app.models import WeatherData, WeatherStats

def calculate_weather_stats():
    """
    Calculate and store weather statistics for each station by year.

    This function aggregates data from the `WeatherData` table to compute:
    - Average maximum temperature
    - Average minimum temperature
    - Total precipitation

    The results are stored in the `WeatherStats` table. The function ensures that
    records with valid data are saved and uses the `merge` operation to prevent duplicates.

    Steps:
    1. Query aggregated statistics grouped by station ID and year.
    2. Iterate over the results to create or update records in the `WeatherStats` table.
    3. Commit the changes to the database.

    Raises:
        Exception: Propagates any database errors during the query or commit.
    """
    # Query to calculate aggregated statistics
    stats = db.session.query(
        WeatherData.station_id,  # Group by station ID
        func.extract('year', WeatherData.date).label('year'),  # Extract year from the date
        func.avg(WeatherData.max_temp).label('avg_max_temp'),  # Average max temperature
        func.avg(WeatherData.min_temp).label('avg_min_temp'),  # Average min temperature
        func.sum(WeatherData.precipitation).label('total_precipitation')  # Total precipitation
    ).group_by(WeatherData.station_id, func.extract('year', WeatherData.date)).all()

    # Iterate over aggregated results
    for station_id, year, avg_max, avg_min, total_precip in stats:
        # Create or update a WeatherStats record
        stat = WeatherStats(
            station_id=station_id,
            year=year,
            avg_max_temp=avg_max if avg_max is not None else None,  # Handle missing max temp
            avg_min_temp=avg_min if avg_min is not None else None,  # Handle missing min temp
            total_precipitation=total_precip if total_precip is not None else None  # Handle missing precipitation
        )
        db.session.merge(stat)  # Merge ensures updates for existing records without duplication

    # Commit all changes to the database
    db.session.commit()