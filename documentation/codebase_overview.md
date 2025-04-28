# Codebase Overview

This document provides a high-level overview of the AircraftHealthML project codebase, its main directories, and the technologies used.

## Project Structure

The project is organized into several key directories:

*   `aircraft_health/aircraft_health/`: Contains the main Django project settings, URL configurations, and core files (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
*   `aircraft_health/aircraft_health/monitoring/`: This is a core Django app containing the backend logic for monitoring. It includes:
    *   `models.py`: Defines the database models (`Flight`, `Stat`). The `Flight` model stores flight records with attributes like `master_index`, `before_after`, `date_diff`, `flight_length`, `label`, `hierarchy`, and `number_flights_before`. The `Stat` model stores statistical records associated with a flight, including the `flight` foreign key, a `key` for the statistic type, and a `value`.
    *   `views.py`: Contains Django views and Django Rest Framework (DRF) views for handling requests and providing API endpoints.
    *   `urls.py`: Defines URL patterns for the monitoring app.
    *   `serializers.py`: Defines DRF serializers for converting model instances to JSON.
    *   `admin.py`: Configuration for the Django admin interface.
    *   `management/commands/`: Contains custom Django management commands, such as `load_flight_data.py` for data ingestion. This command includes a detailed docstring within its `handle` method explaining its functionality.
*   `aircraft_health/aircraft_health/monitoring/frontend/src/`: Contains the source code for the React frontend application.
*   `aircraft_health/aircraft_health/monitoring/ml_models/`: This directory houses the machine learning components, including:
    *   `Models/`: Contains the ML model implementations (`anomaly_detection.py`, `evaluation.py`). Note that `component_degredation_detection.py` and `maintenance_detection.py` appear to be empty placeholders.
    *   `Preprocessing/`: Contains scripts for data preprocessing (`preprocessing_ADAPT.py`, `preprocessing_NGAFID.py`).
    *   `data/`: Contains raw and processed data used by the ML models.
    *   `Testing/`: Contains scripts related to model testing and training.
    *   `utils/`: Contains utility functions for data loading and metrics.

## Technologies Used

The project utilizes a combination of technologies:

*   **Backend:** Django and Django Rest Framework (Python) for the web application backend and API.
*   **Frontend:** React (JavaScript) for the user interface.
*   **Machine Learning:** Python libraries including scikit-learn (Isolation Forest), PyTorch (Transformer), pandas, and numpy for data processing and anomaly detection.
*   **Database:** SQLite (based on `db.sqlite3` file presence).
*   **Data Handling:** CSV and potentially other formats for data storage and processing.

This structure separates the web application concerns (backend and frontend) from the machine learning components, allowing for modular development and potential scaling.