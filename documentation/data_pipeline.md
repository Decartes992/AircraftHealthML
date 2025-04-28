# Data Pipeline

The data pipeline in the AircraftHealthML project involves loading, preprocessing, and utilizing data for machine learning models and the web application.

## Data Sources

The project appears to handle data from at least two sources:

1.  **ADAPT Data:** Time-series data, likely related to sensor readings from aircraft components. Raw data files are in `.txt` format (`aircraft_health/aircraft_health/monitoring/ml_models/data/ADAPT/raw/`).
2.  **NGAFID Data:** Tabular data, likely related to flight headers and characteristics. Raw data files are in `.csv` format (`aircraft_health/aircraft_health/monitoring/ml_models/data/NGAFID/raw/`).

## Data Ingestion

*   **NGAFID Data:** The `load_flight_data.py` management command (`aircraft_health/aircraft_health/monitoring/management/commands/load_flight_data.py`) is responsible for loading `flight_header.csv` data into the Django database models (`Flight` and `Stat`).
*   **ADAPT Data:** The loading of raw ADAPT `.txt` files is handled by the `ADAPTPreprocessor` class in `preprocessing_ADAPT.py`.

## Data Preprocessing

Preprocessing is handled separately for ADAPT and NGAFID data:

*   **ADAPT Preprocessing (`preprocessing_ADAPT.py`):**
    *   Loads raw `.txt` experiment files, skipping metadata.
    *   Extracts fault injection information, including time, component, type, location, and duration.
    *   Processes sensor data, specifically 'AntagonistData' rows and columns starting with 'E' (voltage).
    *   Converts relevant columns to numeric types, coercing errors.
    *   Handles missing values using a rolling mean imputation (5-period window).
    *   Saves processed sensor data and extracted fault information to separate `.csv` files in the `processed` directory (`aircraft_health/aircraft_health/monitoring/ml_models/data/ADAPT/processed/`).
    *   Generates and saves summary statistics for individual experiments and a combined summary for all processed data.
*   **NGAFID Preprocessing (`preprocessing_NGAFID.py`):**
    *   Loads the `flight_header.csv` file.
    *   Handles missing values: numerical columns are imputed with the mean, and categorical columns (specifically 'hierarchy') are handled with a mapping based on the 'label' column or imputed with the mode if 'label' is missing.
    *   Detects and handles outliers in the 'flight_length' column using the Interquartile Range (IQR) method.
    *   Performs feature engineering, including calculating mean flight length per label, creating a time-based feature (`is_recent_flight`), adding a ratio of flight length to the number of previous flights (`flight_length_ratio`), and creating `flights_per_length` and `before_after_date_diff` features.
    *   Handles infinite values in engineered features by replacing them with NaN and then imputing with the mean.
    *   Clips negative values in 'number_flights_before' to 0.
    *   Encodes the 'label' column using `LabelEncoder`, creating a new 'label_encoded' column.
    *   Normalizes specified numerical features ('flight_length', 'number_flights_before', 'date_diff') using either StandardScaler or MinMaxScaler (MinMaxScaler is used in the main execution block). A log transformation is applied to 'date_diff' before normalization.
    *   Splits the data into training and testing sets using stratified sampling based on the target column ('label_encoded').
    *   Saves intermediate results at various stages of preprocessing and the final processed data to `.csv` files in the `intermediate` and `processed` directories respectively (`aircraft_health/aircraft_health/monitoring/ml_models/data/NGAFID/processed/`).

## Data Flow

Raw data files are ingested and then preprocessed by the respective scripts. The processed data is saved and then used as input for the machine learning models located in the `ml_models/Models/` directory. The results from the ML models are then saved and accessed by the Django backend (`monitoring/views.py`) to be displayed in the React frontend.