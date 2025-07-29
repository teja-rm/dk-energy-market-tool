# Danish Energy Market Analysis Tool

A professional Python application for analyzing Danish electricity market data from Energinet's public APIs. Built to demonstrate advanced data engineering, statistical analysis, and market intelligence capabilities for Nordic energy markets.

## Overview

This tool fetches, processes, and analyzes Danish electricity spot prices to identify trading patterns, price trends, and market opportunities. The application provides automated data ingestion, statistical modeling, and professional PDF reporting with embedded visualizations.

**Key Value Proposition:** Transform raw energy market data into actionable insights through robust statistical analysis and automated reporting.

## Features

- **Real-time Data Integration**: Automated fetching from Energinet's Energi Data Service API with rate limiting
- **Statistical Analysis**: ARIMA forecasting, volatility analysis, and market pattern detection  
- **Professional Reporting**: Automated PDF generation with embedded matplotlib visualizations
- **Production Architecture**: Modular design with comprehensive testing and error handling
- **Deployment Ready**: Docker support, CI/CD pipeline, and monitoring capabilities

## Quick Start


### Prerequisites

- Python 3.11+
- Git

## Installation

Clone the repository and install dependencies:

```bash
git clone [dk-energy-market-tool.git]
cd dk-energy-market-tool
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install .
```

## How to Run

Run the main pipeline (fetch, transform, analyze, report):

```bash
python -m dkenergy --full
```

This will fetch the latest data, perform analysis, and generate an HTML report in `data/reports/`.

## Docker

Docker configuration is included for production deployment. See `Dockerfile` and `docker-compose.yml` in the repo.


