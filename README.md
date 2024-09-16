# Air Quality Ingestion Pipeline

This project implements a data ingestion pipeline that retrieves weather and air quality data for various cities in Cameroon using the OpenWeatherMap API. The collected data is transformed and saved to an Amazon S3 bucket using Prefect for workflow orchestration.

## Project Structure

AIR-QUALITY-INGESTION-PIPELINE
│
├── data/
├── pipelines/
│   └── data_ingestion.py
├── README.md
├── requirements.txt
└── Dockerfile
