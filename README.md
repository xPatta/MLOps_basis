# MLOps_basis
Automated Machine Learning pipeline scaffold. <br>
Starting from the Coursera MLOps specialization: https://www.coursera.org/specializations/machine-learning-operations-mlops.

# Setup
- Docker Compose set up to accept multi-service applications. <br>
    Currently only the ML pipeline is implemented as single service (i.e. single image), likely to be extended with MLflow and a DB managing system.
- Dockerfile defining the ML pipeline as multi-stage image:
    1. Builds environment with dependencies
    2. Tests the data validation pipeline with PyTest
    3. (If tests succeed) Runs the ML pipeline
- ```src/MLOps/ML_pipeline.py``` defines the whole ML pipeline, as:
    1. Data generation
    2. Data validation
    3. ... to be extended with feature engineering and ML model run


# Usage
Just run ```docker compose up --build``` from the main repository, and docker-compose will complete every step described above