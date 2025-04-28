# Chatbot Guide: AircraftHealthML Project

This guide provides a concise overview of the AircraftHealthML project, intended for use as a reference for a chatbot or quick lookup. It synthesizes key information about the project's goal, technologies, data sources, core components, and provides pointers to more detailed documentation.

## Project Goal & Overview

The AircraftHealthML project aims to develop a system for monitoring the health of aircraft components using machine learning techniques. It processes flight data from various sources to detect anomalies and provide insights into potential maintenance needs. The project includes a web application for visualizing data and results.

## Key Technologies Used

*   **Backend:** Django, Django Rest Framework (Python)
*   **Frontend:** React (JavaScript)
*   **Machine Learning:** Python libraries including scikit-learn (Isolation Forest), PyTorch (Transformer), pandas, numpy
*   **Database:** SQLite

## Data Sources

The project utilizes data from two primary sources:

*   **ADAPT Data:** Time-series sensor data from aircraft components.
*   **NGAFID Data:** Tabular flight header and characteristic data.

Detailed information on data handling and preprocessing can be found in the [Data Pipeline documentation](data_pipeline.md).

## Core Components Identified

The project is structured into several key components:

*   **Django Backend (`aircraft_health/aircraft_health/monitoring/`):** Handles data models, API endpoints, and backend logic.
*   **React Frontend (`aircraft_health/aircraft_health/monitoring/frontend/src/`):** Provides the user interface for data visualization and interaction.
*   **Machine Learning Models (`aircraft_health/aircraft_health/monitoring/ml_models/`):** Contains the implementations for anomaly detection using Transformer (ADAPT) and Isolation Forest (NGAFID) models.
*   **Data Ingestion and Preprocessing:** Scripts and management commands for loading and preparing data from ADAPT and NGAFID sources.

More details on the codebase structure are available in the [Codebase Overview](codebase_overview.md).

## Pointers to Main Documentation Files

For more in-depth information, refer to the following documents in the `/documentation/` directory:

*   [Codebase Overview](codebase_overview.md): Detailed breakdown of the project's directory structure and components.
*   [Data Pipeline](data_pipeline.md): Explanation of data sources, ingestion, and preprocessing steps.
*   [Machine Learning Models](ml_models.md): Description of the ML models used, their purpose, and implementation details.
*   [Web Application Integration](webapp_integration.md): How the backend and frontend are integrated.
*   [API Endpoints](api_endpoints.md): List and description of the available API endpoints.