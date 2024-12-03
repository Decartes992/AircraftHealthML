# preprocessing_ADAPT.py

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional
import logging
from datetime import datetime
import os 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ADAPTPreprocessor:
    def __init__(self, data_dir: str = "../data/ADAPT"):
        """
        Initialize ADAPT preprocessor
        
        Args:
            data_dir: Base directory for ADAPT data
        """
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True) 
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Define sensor types based on paper
        self.sensor_prefixes = {
            'E': 'voltage',
            'ESH': 'relay_position',
            'ISH': 'current',
            'IT': 'temperature', 
            'LT': 'load',
            'ST': 'status',
            'TE': 'temperature'
        }
        
        # Known fault types from paper
        self.fault_types = {
            'StuckAt': 'stuck',
            'FailedOpen': 'failed_open',
            'FailedOff': 'failed_off',
            'Noise': 'noise',
            'Drift': 'drift'
        }

    def load_experiment(self, filename: str) -> pd.DataFrame:
        """
        Load a single ADAPT experiment file
        
        Args:
            filename: Name of experiment file
            
        Returns:
            DataFrame containing experiment data
        """
        try:
            file_path = self.raw_dir / filename
            
            # Check if file exists
            if not file_path.exists():
                raise FileNotFoundError(f"File not found at {file_path}")
                
            # Read data with tab delimiter, skipping metadata
            df = pd.read_csv(file_path, delimiter='\t', skiprows=1, header=0, encoding='utf-8')  # Adjusted skiprows and header
            
            # Print columns for debugging
            logger.info(f"Columns in DataFrame: {df.columns.tolist()}")
            
            if 'Time' not in df.columns:
                # Try alternative column names
                time_columns = [col for col in df.columns if 'time' in col.lower()]
                if time_columns:
                    df = df.rename(columns={time_columns[0]: 'Time'})
                else:
                    raise KeyError("No time column found in the data")
            
            # Print first few rows for debugging
            logger.info(f"First few rows of Time column:\n{df['Time'].head()}")
            
            try:
                # Convert timestamp with error handling
                df['Time'] = pd.to_datetime(df['Time'], 
                                        format='%Y-%m-%d %H:%M:%S.%f %Z',
                                        errors='coerce')
            except ValueError as e:
                logger.warning(f"Error converting time with initial format, trying alternative: {str(e)}")
                # Try alternative format without timezone
                df['Time'] = pd.to_datetime(df['Time'], 
                                        format='%Y-%m-%d %H:%M:%S.%f',
                                        errors='coerce')
            
            # Check for any NaT values after conversion
            if df['Time'].isna().any():
                logger.warning("Some timestamp conversions resulted in NaT values")
                
            logger.info(f"Successfully loaded {filename}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            logger.error(f"Full error details:", exc_info=True)
            raise


    def extract_fault_info(self, df: pd.DataFrame) -> Dict:
        """
        Extract fault injection information from experiment data
        
        Args:
            df: Raw experiment DataFrame
            
        Returns:
            Dictionary containing fault details
        """
        fault_info = {
            'time': None,
            'component': None, 
            'type': None,
            'location': None,
            'duration': None
        }
        
        # Find FaultInject rows
        fault_rows = df[df['SensorData'] == 'FaultInject']
        
        if not fault_rows.empty:
            fault_row = fault_rows.iloc[0]
            
            # Extract fault information
            fault_info['time'] = fault_row['Time']
            fault_info['component'] = next((col for col in fault_row.index 
                                          if not pd.isna(fault_row[col]) and 
                                          col.startswith(('E', 'ESH', 'ISH'))), None)
            fault_info['type'] = fault_row['FaultType'] if 'FaultType' in fault_row else None
            fault_info['location'] = fault_row['FaultLocation'] if 'FaultLocation' in fault_row else None
            
            # Calculate duration if experiment end time exists
            if not df.empty:
                fault_info['duration'] = (df['Time'].max() - fault_info['time']).total_seconds()
        
        return fault_info

    def process_sensor_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process sensor readings from experiment data
        
        Args:
            df: Raw experiment DataFrame
            
        Returns:
            DataFrame containing processed sensor data
        """
        # Filter antagonist data (actual sensor readings)
        sensor_data = df[df['SensorData'] == 'AntagonistData'].copy()
        
        # Get sensor columns
        sensor_cols = [col for col in sensor_data.columns 
                      if any(col.startswith(prefix) for prefix in self.sensor_prefixes.keys())]
        
        # Keep time and sensor columns
        processed_data = sensor_data[['Time'] + sensor_cols]
        
        # Convert sensor readings to float where possible
        for col in sensor_cols:
            processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce')
            
        # Forward fill missing values
        processed_data = processed_data.ffill()
        
        return processed_data

    def preprocess_experiment(self, filename: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Main preprocessing function for a single experiment
        
        Args:
            filename: Name of experiment file
            
        Returns:
            Tuple of (processed sensor DataFrame, fault information dict)
        """
        file_path = self.raw_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        # Load raw data
        raw_df = self.load_experiment(filename)
        
        # Extract fault information
        fault_info = self.extract_fault_info(raw_df)
        
        # Process sensor data
        processed_df = self.process_sensor_data(raw_df)
        
        # Save processed data
        output_filename = f"processed_{filename.replace('.txt', '.csv')}"
        processed_df.to_csv(self.processed_dir / output_filename, index=False)
        
        # Save fault info
        fault_info_df = pd.DataFrame([fault_info])
        fault_info_df.to_csv(self.processed_dir / f"fault_info_{filename.replace('.txt', '.csv')}", 
                            index=False)
        
        logger.info(f"Processed data saved to {output_filename}")
        
        return processed_df, fault_info

    def preprocess_all_experiments(self) -> None:
        """Process all raw experiment files in the raw directory"""
        raw_files = list(self.raw_dir.glob('*.txt'))
        
        for file in raw_files:
            try:
                logger.info(f"Processing {file.name}")
                self.preprocess_experiment(file.name)
            except FileNotFoundError as e:
                logger.error(f"Error: {e}")
            except Exception as e:
                logger.error(f"Error processing {file.name}: {str(e)}")
                continue

def main():
    """Main execution function"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    data_dir = os.path.join(project_root, "ml_models", "data", "ADAPT")
    
    logger.info(f"Project root: {project_root}")
    logger.info(f"Data directory: {data_dir}")
    
    preprocessor = ADAPTPreprocessor(data_dir=data_dir)
    
    # Process all experiments
    preprocessor.preprocess_all_experiments()

if __name__ == "__main__":
    main()