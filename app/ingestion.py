import os
import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import WeatherData

def ingest_weather_data(filename=None):
    """
    Ingest weather data from a specified file or the wx_data directory located parallel to the app directory.
    """
    # Counters for logging
    inserted_count = 0
    updated_count = 0
    skipped_count = 0

    # Logging configuration
    logging.basicConfig(level=logging.INFO)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Get file paths
    if filename:
        file_paths = [filename]
    else:
        data_dir = os.path.join(base_dir, '..', 'wx_data')
        if not os.path.exists(data_dir):
            logging.error(f"Data directory does not exist: {data_dir}")
            return
        file_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".txt")]

    logging.info(f"Starting data ingestion at {datetime.now()}")
    for filepath in file_paths:
        if not os.path.exists(filepath):
            logging.error(f"File does not exist: {filepath}")
            continue

        logging.info(f"Processing file: {filepath}")
        station_id = os.path.basename(filepath).split('.')[0]

        try:
            with open(filepath, 'r') as file:
                for line in file:
                    try:
                        date, max_temp, min_temp, precip = line.strip().split('\t')

                        # Handle missing values
                        max_temp = None if max_temp == '-9999' else int(max_temp) / 10
                        min_temp = None if min_temp == '-9999' else int(min_temp) / 10
                        precip = None if precip == '-9999' else int(precip) / 10

                        # Convert date
                        date_obj = datetime.strptime(date, '%Y%m%d').date()

                        # Check for existing record
                        existing_data = WeatherData.query.filter_by(station_id=station_id, date=date_obj).first()
                        if existing_data:
                            # Update existing record
                            existing_data.max_temp = max_temp
                            existing_data.min_temp = min_temp
                            existing_data.precipitation = precip
                            updated_count += 1
                        else:
                            # Insert new record
                            weather = WeatherData(
                                station_id=station_id,
                                date=date_obj,
                                max_temp=max_temp,
                                min_temp=min_temp,
                                precipitation=precip
                            )
                            db.session.add(weather)
                            inserted_count += 1
                    except ValueError as ve:
                        logging.warning(f"Skipping invalid line in file {filepath}: {line.strip()} - {ve}")
                        skipped_count += 1
                    except IntegrityError as ie:
                        db.session.rollback()
                        logging.warning(f"Integrity error for line: {line.strip()} - {ie}")
                        skipped_count += 1
        except FileNotFoundError as fnf_error:
            logging.error(f"File not found: {filepath} - {fnf_error}")
            continue

    try:
        db.session.commit()
        logging.info(f"Data ingestion completed at {datetime.now()}")
        logging.info(f"Total records inserted: {inserted_count}")
        logging.info(f"Total records updated: {updated_count}")
        logging.info(f"Total records skipped: {skipped_count}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to commit data to the database: {e}")