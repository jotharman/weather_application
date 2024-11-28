import os
import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import WeatherData

# Logging configuration
logging.basicConfig(level=logging.INFO)

def get_file_paths(base_dir, filename=None, dir_path=None, file_extension=".txt"):
    """
    Retrieve file paths for weather data ingestion.

    Args:
        base_dir (str): Base directory of the script.
        filename (str, optional): Specific file name to process. Defaults to None.
        dir_path (str, optional): Directory path containing weather files. Defaults to 'wx_data'.
        file_extension (str, optional): File extension filter. Defaults to ".txt".

    Returns:
        list: List of file paths matching the criteria.
    """
    if filename:
        return [filename]
    
    # Use the provided directory path or default to 'wx_data'
    data_dir = dir_path if dir_path else os.path.join(base_dir, '..', 'wx_data')
    
    if not os.path.exists(data_dir):
        logging.error(f"Data directory does not exist: {data_dir}")
        return []
    
    return [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(file_extension)]


def parse_weather_line(line):
    """
    Parse a line of weather data into structured format.

    Args:
        line (str): A single line from the weather data file.

    Returns:
        tuple: Parsed date, max temperature, min temperature, and precipitation.

    Raises:
        ValueError: If the line format is invalid.
    """
    try:
        date, max_temp, min_temp, precip = line.strip().split('\t')
        # Handle missing values
        max_temp = None if max_temp == '-9999' else int(max_temp) / 10
        min_temp = None if min_temp == '-9999' else int(min_temp) / 10
        precip = None if precip == '-9999' else int(precip) / 10
        date_obj = datetime.strptime(date, '%Y%m%d').date()
        return date_obj, max_temp, min_temp, precip
    except ValueError as ve:
        raise ValueError(f"Invalid line format: {line.strip()} - {ve}")


def process_file(filepath):
    """
    Process a single weather data file to update or insert records into the database.

    Args:
        filepath (str): Path to the weather data file.

    Returns:
        tuple: Counts of inserted, updated, and skipped records.
    """
    inserted_count = 0
    updated_count = 0
    skipped_count = 0

    station_id = os.path.basename(filepath).split('.')[0]

    try:
        with open(filepath, 'r') as file:
            for line in file:
                try:
                    date, max_temp, min_temp, precip = parse_weather_line(line)

                    # Check for existing record
                    existing_data = WeatherData.query.filter_by(
                        station_id=station_id, date=date
                    ).first()
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
                            date=date,
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

        return inserted_count, updated_count, skipped_count
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {filepath} - {fnf_error}")
        return 0, 0, 1


def ingest_weather_data(filename=None):
    """
    Ingest weather data from a specified file or directory of files.

    Args:
        filename (str, optional): Specific file name to ingest. Defaults to None.

    Steps:
        1. Retrieve file paths using `get_file_paths`.
        2. Process each file to update or insert weather data.
        3. Commit changes to the database.

    Logs:
        Logs the number of inserted, updated, and skipped records.

    Raises:
        Exception: Logs and rolls back in case of database commit failure.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = get_file_paths(base_dir, filename)

    if not file_paths:
        logging.error("No valid files found for ingestion.")
        return

    total_inserted = 0
    total_updated = 0
    total_skipped = 0

    logging.info(f"Starting data ingestion at {datetime.now()}")
    for filepath in file_paths:
        logging.info(f"Processing file: {filepath}")
        inserted, updated, skipped = process_file(filepath)
        total_inserted += inserted
        total_updated += updated
        total_skipped += skipped

    try:
        db.session.commit()
        logging.info(f"Data ingestion completed at {datetime.now()}")
        logging.info(f"Total records inserted: {total_inserted}")
        logging.info(f"Total records updated: {total_updated}")
        logging.info(f"Total records skipped: {total_skipped}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to commit data to the database: {e}")


if __name__ == "__main__":
    ingest_weather_data()