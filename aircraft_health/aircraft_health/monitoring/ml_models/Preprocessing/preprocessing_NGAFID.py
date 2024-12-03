import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import os
import logging

def load_data(filepath):
    """
    Load the NGAFID dataset from a CSV file.
    """
    data = pd.read_csv(filepath)
    print("Data Loaded Successfully!")
    print(data.info())
    return data

def handle_missing_values(data):
    """
    Fill missing values or drop irrelevant rows.
    """
    # Fill missing 'hierarchy' with a placeholder
    data['hierarchy'] = data['hierarchy'].fillna('Unknown')
    # Drop rows with excessive missing values
    data = data.dropna(thresh=len(data.columns) - 3)
    print("Missing values handled!")
    return data

def encode_labels(data):
    """
    Encode categorical columns like 'label' and 'hierarchy'.
    """
    label_encoder = LabelEncoder()
    data['label_encoded'] = label_encoder.fit_transform(data['label'])
    data['hierarchy_encoded'] = label_encoder.fit_transform(data['hierarchy'])
    print("Categorical data encoded!")
    return data, label_encoder

def normalize_features(data, columns_to_normalize):
    """
    Normalize numeric columns using StandardScaler.
    """
    scaler = StandardScaler()
    data[columns_to_normalize] = scaler.fit_transform(data[columns_to_normalize])
    print("Numeric data normalized!")
    return data, scaler

def feature_engineering(data):
    """
    Add new features based on existing data.
    """
    # Mean flight length per label
    data['mean_flight_length_per_label'] = data.groupby('label')['flight_length'].transform('mean')
    # Time-based feature
    data['is_recent_flight'] = data['date_diff'].apply(lambda x: 1 if x > 0 else 0)
    print("Feature engineering complete!")
    return data

def split_data(data, target_column):
    """
    Split data into train and test sets.
    """
    X = data.drop(columns=[target_column, 'label', 'hierarchy', 'Master Index'])
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Data split into train and test sets!")
    return X_train, X_test, y_train, y_test

def preprocess_ngafid(filepath, target_column, columns_to_normalize):
    """
    Full preprocessing pipeline for NGAFID data.
    """
    data = load_data(filepath)
    data = handle_missing_values(data)
    data, label_encoder = encode_labels(data)
    data, scaler = normalize_features(data, columns_to_normalize)
    data = feature_engineering(data)
    X_train, X_test, y_train, y_test = split_data(data, target_column)
    return X_train, X_test, y_train, y_test, label_encoder, scaler, data

if __name__ == "__main__":
    # Main execution function
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    data_dir = os.path.join(project_root, "ml_models",  "data", "NGAFID", "raw")
    processed_data_dir = os.path.join(project_root, "ml_models","data", "NGAFID",  "processed")
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Project root: {project_root}")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Processed data directory: {processed_data_dir}")
    
    filepath = os.path.join(data_dir, "flight_header.csv")
    
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
    else:
        target_column = "label_encoded"
        columns_to_normalize = ['flight_length', 'number_flights_before', 'date_diff']
        
        X_train, X_test, y_train, y_test, label_encoder, scaler, processed_data = preprocess_ngafid(
            filepath, target_column, columns_to_normalize
        )
        
        # Save the processed data
        os.makedirs(processed_data_dir, exist_ok=True)
        processed_filepath = os.path.join(processed_data_dir, "processed_flight_header.csv")
        processed_data.to_csv(processed_filepath, index=False)
        
        print("Preprocessing Complete!")
        logger.info(f"Processed data saved to: {processed_filepath}")
