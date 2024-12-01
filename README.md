# **AircraftHealthML**

## **Overview**
AircraftHealthML is a machine learning project focused on integrated aircraft health monitoring, predictive maintenance, and component interaction analysis. Leveraging advanced machine learning techniques and multi-source datasets, the project aims to predict failures, analyze cascading faults, and optimize maintenance strategies in aviation systems.

## **Features**
- Anomaly detection for fault identification.
- Predictive maintenance using time-series modeling.
- Component interaction analysis with graph-based methods.
- Integration of multiple datasets for unified diagnostics.
- Comprehensive evaluation and optimization of machine learning models.

## **Datasets**
This project utilizes publicly available datasets:
1. **NASA ADAPT Dataset**: Electrical power system fault scenarios.
2. **NGAFID Maintenance Logs**: Annotated time-series data linked to unplanned maintenance events.
3. **Engine Run-to-Failure Dataset**: Real-world degradation trajectories for aircraft engines.

## **Technologies Used**
- **Machine Learning Models**:
  - Isolation Forest, One-Class SVM (Anomaly Detection)
  - LSTMs, Bayesian Networks, Gaussian Processes (Predictive Maintenance)
  - Graph Neural Networks (Component Interaction Analysis)
- **Data Preprocessing**:
  - Principal Component Analysis (PCA)
  - Recursive Feature Elimination (RFE)
  - Data Normalization and Fusion
- **Programming and Tools**:
  - Python, NumPy, Pandas, Matplotlib, Scikit-learn, TensorFlow, PyTorch

## **Tentative Project Structure**
```
AircraftHealthML/
├── data/               # Scripts for dataset preprocessing
├── models/             # Implementation of machine learning models
├── notebooks/          # Jupyter Notebooks for analysis and testing
├── results/            # Output files, evaluation metrics, and visualizations
├── utils/              # Helper scripts for feature engineering and data integration
├── README.md           # Project description and instructions
├── requirements.txt    # Dependencies for the project
```

## **How to Run**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AircraftHealthML.git
   cd AircraftHealthML
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Preprocess datasets:
   ```bash
   python data/preprocess.py
   ```
4. Train models:
   ```bash
   python models/train.py
   ```
5. Generate results:
   ```bash
   python results/evaluate.py
   ```

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## **Acknowledgments**
Special thanks to NASA, NGAFID, and other sources for providing datasets, and to Dr. Issam Hammad for guidance in this project.
