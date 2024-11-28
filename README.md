# Weather Data API

This project provides an API for managing and analyzing weather data. It allows ingestion of data, database management, and API-based interactions.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+**
2. **pip** (Python package installer)
3. **PostgreSQL** (if using locally; can be replaced with a managed database like AWS RDS)
4. **Virtual Environment** (optional but recommended)

---

## Setup Instructions


git clone https://github.com/jotharman/weather_application.git
cd weather_application/

## Install Dependencies

## Set up a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  
Install required Python packages:
pip install -r requirements.txt

## Configure the Database
## Database Initialization:
## Open config.py and configure your database URI. For example:

SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/weather_db'

## Create the Database:
## Run the following commands in the Flask shell to initialize the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

## Ingest and Analyze Data

## Open the Flask shell:
flask shell
from app import ingest_weather_data, analyze_weather_data
## Import and run data ingestion:
ingest_weather_data()  ##give the name of the folder with data to ingest
## Optionally analyze the data using:
analyze_weather_data()  




## Run the Application
python run.py

## Access the application at
http://127.0.0.1:5000

## Running Tests

pytest



