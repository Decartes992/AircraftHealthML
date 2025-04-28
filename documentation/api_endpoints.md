# API Endpoints

The AircraftHealthML project exposes several API endpoints through its Django Rest Framework backend, primarily located in `aircraft_health/aircraft_health/monitoring/views.py` and configured in `aircraft_health/aircraft_health/monitoring/urls.py`. These endpoints facilitate communication between the React frontend and the backend logic, including data retrieval, analysis, and access to ML model results.

Below is a list of identified API endpoints and their purposes:

*   **`/api/experiments/`** (GET)
    *   **Purpose:** Retrieves a list of available ADAPT experiment files from the raw data directory. Returns a JSON response containing a list of experiment filenames. Returns an error message with status 500 if an exception occurs.
    *   **View Function:** `get_experiment_list` in `views.py`.
*   **`/api/experiments/<str:experiment_id>/`** (GET)
    *   **Purpose:** Retrieves and processes detailed data for a specific ADAPT experiment file. Returns a JSON response containing sensor data and experiment info. Handles file not found (404), invalid format (400), and other errors (500).
    *   **Parameters:** `experiment_id` (string) - the filename of the experiment.
    *   **View Function:** `get_experiment_data` in `views.py`.
*   **`/api/labels/`** (GET)
    *   **Purpose:** Returns a list of unique flight labels present in the database. `get_unique_labels` returns a JSON response containing a list of unique labels. `unique_labels` returns a DRF Response containing a list of unique labels and their counts.
    *   **View Function:** `get_unique_labels` and `unique_labels` in `views.py`.
*   **`/api/flights/label/<str:label>/`** (GET)
    *   **Purpose:** Filters and returns flight data from the database based on a specific label. `filter_flights_by_label` returns a JSON response containing a list of filtered flights. `flights_by_label` returns a JSON response containing flight entries and base64 encoded visualizations, and returns an error message with status 500 if an exception occurs.
    *   **Parameters:** `label` (string) - the flight label to filter by.
    *   **View Function:** `filter_flights_by_label` and `flights_by_label` in `views.py`.
*   **`/api/flights/data/label/<str:label>/`** (GET)
    *   **Purpose:** Returns serialized flight data for a given label using the `FlightSerializer`. Returns a DRF Response containing the serialized data.
    *   **Parameters:** `label` (string) - the flight label.
    *   **View Function:** `flight_data_by_label` in `views.py`.
*   **`/api/flights/insights/<str:label>/`** (GET)
    *   **Purpose:** Provides basic statistical insights (average, max, min flight length) for flights associated with a specific label. Returns a JSON response containing these insights. Returns an error message with status 500 if an exception occurs.
    *   **Parameters:** `label` (string) - the flight label.
    *   **View Function:** `flight_insights` in `views.py`.
*   **`/api/flights/grouped/`** (GET)
    *   **Purpose:** Returns flight data grouped by label, intended for visualization purposes (scatter and histogram data) on the frontend. Returns a DRF Response.
    *   **Query Parameters:** `label` (string) - the flight label to group by.
    *   **View Function:** `grouped_flight_data` in `views.py`.
*   **`/api/flights/preprocessed/<str:label>/`** (GET)
    *   **Purpose:** Returns preprocessed flight data (scatter, histogram) and associated insights (average, max, min flight length) for a given label. Returns a DRF Response.
    *   **Parameters:** `label` (string) - the flight label.
    *   **View Function:** `preprocessed_flight_data` in `views.py`.
*   **`/api/anomaly-results/`** (GET)
    *   **Purpose:** Retrieves anomaly detection results for both ADAPT and NGAFID data from the saved JSON result files. Returns a JSON response containing results for both models. Handles file not found (404) and other errors (500). Replaces NaN values with None.
    *   **View Function:** `get_anomaly_results` in `views.py`.
*   **`/api/update-threshold/`** (POST)
    *   **Purpose:** Allows updating the anomaly detection threshold. Validates the threshold value and returns success/error response. Returns status 400 for invalid requests and 500 for unexpected errors.
    *   **Request Body:** JSON object containing the `threshold` value (required).
    *   **View Function:** `update_threshold` in `views.py`.
*   **`/api/historical-data/`** (GET)
    *   **Purpose:** Retrieves historical anomaly data based on a specified date range.
    *   **Query Parameters:** `start` (date string), `end` (date string).
    *   **View Function:** `get_historical_data` in `views.py`.
*   **`/api/flights/`** (GET)
    *   **Purpose:** Lists all flights with options for searching, filtering by `before_after` and `label`, and ordering by `date_diff` and `flight_length`.
    *   **View Class:** `FlightListView` in `views.py`.
*   **`/api/flights/<int:flight_id>/`** (GET)
    *   **Purpose:** Retrieves detailed information for a specific Flight instance by its master_index. Returns a DRF Response containing the serialized Flight data. Returns a 404 response if the Flight is not found, or a 500 response if an unexpected error occurs.
    *   **Parameters:** `flight_id` (integer) - the master index of the flight.
    *   **View Class:** `FlightDetailView` in `views.py`.

These API endpoints provide the necessary interface for the frontend to interact with the backend data and ML model results, enabling the visualization and monitoring of aircraft health.