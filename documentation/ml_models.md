# Machine Learning Models

This document details the machine learning models identified in the AircraftHealthML project codebase, their purpose, inputs/outputs, and associated libraries.

The primary ML logic is contained within the `aircraft_health/aircraft_health/monitoring/ml_models/Models/` directory, specifically in `anomaly_detection.py`. The files `component_degredation_detection.py` and `maintenance_detection.py` are present but appear to be empty placeholders.

## Anomaly Detection (`anomaly_detection.py`)

This module implements a hybrid anomaly detection approach designed to handle both time-series ADAPT data and tabular NGAFID data.

### Models Used

*   **ADAPT Anomaly Detector (`ADAPTAnomalyDetector`):**
    *   **Type:** Transformer-based model.
    *   **Purpose:** Detect anomalies in ADAPT time-series data by learning normal patterns and identifying deviations. It uses a Multi-Head Attention mechanism to capture temporal dependencies.
    *   **Inputs:** Scaled time-series data (PyTorch Tensor).
    *   **Outputs:** Reconstructed time-series data (PyTorch Tensor). Anomaly detection is based on the reconstruction error.
    *   **Libraries:** PyTorch (`torch`, `torch.nn`), numpy.
*   **NGAFID Anomaly Detector (`NGAFIDAnomalyDetector`):**
    *   **Type:** Isolation Forest.
    *   **Purpose:** Detect anomalies in NGAFID tabular data. Isolation Forest works by isolating observations, and anomalies are more susceptible to isolation.
    *   **Inputs:** Scaled tabular data (pandas DataFrame).
    *   **Outputs:** Anomaly predictions (-1 for anomalies, 1 for inliers) and anomaly scores (lower scores indicate higher anomaly likelihood).
    *   **Libraries:** scikit-learn (`IsolationForest`, `StandardScaler`), pandas, numpy.

### Hybrid Anomaly Detector (`HybridAnomalyDetector`)

This class orchestrates the use of both the ADAPT and NGAFID anomaly detectors.

*   **Purpose:** Provides a unified interface for training and detecting anomalies in both datasets. It manages the scaling and application of the appropriate model based on the input data format.
*   **Key Methods:**
    *   `__init__`: Initializes the ADAPT and NGAFID detectors, scalers, and hyperparameters.
    *   `validate_data`: Checks for NaN, infinity, or excessively large values in the input data.
    *   `fit_adapt`: Trains the ADAPT detector using scaled time-series data via a DataLoader. Uses MSE loss and Adam optimizer.
    *   `fit_ngafid`: Trains the NGAFID detector (Isolation Forest) on scaled tabular data.
    *   `detect_adapt_anomalies`: Detects anomalies in ADAPT data based on reconstruction error and a dynamic threshold calculated from a rolling mean and standard deviation.
    *   `detect_ngafid_anomalies`: Detects anomalies in NGAFID data using the Isolation Forest's `predict` method.
    *   `get_adapt_anomaly_scores`: Calculates reconstruction errors for ADAPT data.
    *   `get_ngafid_anomaly_scores`: Calculates anomaly scores for NGAFID data using the Isolation Forest's `decision_function`.
    *   `save_models`: Saves the trained ADAPT (state dict and scaler) and NGAFID (detector) models using `torch.save` and `joblib.dump`.
    *   `load_models`: Loads the saved models.
    *   `save_detection_results`: Formats and saves the anomaly detection results (time series data, anomalies, scores, timeline, summary) for both ADAPT and NGAFID data to JSON files in a specified results directory.
    *   `fit`: Unified fit method that calls either `fit_adapt` or `fit_ngafid` based on the input data shape.
    *   `predict`: Unified predict method that calls either `detect_adapt_anomalies` or `detect_ngafid_anomalies`.
*   **Libraries:** pandas, numpy, PyTorch, scikit-learn, joblib, json, pathlib, logging.

## Evaluation (`evaluation.py`)

This module provides tools for evaluating the performance of anomaly detection models.

*   **Anomaly Evaluator (`AnomalyEvaluator`):**
    *   **Purpose:** Provides methods for normalizing scores, finding optimal thresholds, cross-validating models, calculating various evaluation metrics (precision, recall, F1-score, ROC AUC, PR AUC), and plotting results (confusion matrix, ROC curve, precision-recall curve, score distributions, threshold sensitivity).
    *   **Libraries:** numpy, pandas, scikit-learn (`roc_curve`, `auc`, `precision_recall_curve`, `confusion_matrix`, `classification_report`), matplotlib, logging, typing.

## Data Loading Utility (`utils/data_loader.py`)

While not a model itself, `data_loader.py` contains the `load_adapt_data` function, which is crucial for preparing ADAPT data for the anomaly detection model.

*   **`load_adapt_data` function:**
    *   **Purpose:** Loads, combines, and resamples all processed ADAPT `.csv` files.
    *   **Process:** Reads all `processed_*.csv` files from the specified directory, converts the 'Time' column to datetime objects, sets 'Time' as the index, resamples the data to 1-second intervals (mean), interpolates missing values linearly, and concatenates the dataframes.
    *   **Libraries:** pandas, numpy, pathlib, logging.