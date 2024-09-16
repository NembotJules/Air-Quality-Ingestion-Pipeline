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


- `data/`: Directory where the combined data will be stored.
- `pipelines/`: Contains the main Python script for data ingestion (`data_ingestion.py`).
- `README.md`: Documentation for the project.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `Dockerfile`: Configuration file for building the Docker image.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your machine.
- An account with [OpenWeatherMap](https://openweathermap.org/) to obtain an API key.
- An [AWS](https://aws.amazon.com/) account to create an S3 bucket and obtain access keys.

## Setup

1. **Create an S3 Bucket:**
   Ensure you have an S3 bucket named `zeguild-bucket` in your AWS account. This is where the combined data will be stored.

2. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd AIR-QUALITY-INGESTION-PIPELINE

