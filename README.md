# EcoGuardian Fog

A fog computing node for the EcoGuardian IoT ecosystem that provides edge analytics and metric aggregation for environmental monitoring devices.

## Overview

EcoGuardian Fog is a lightweight fog computing application built with Flask that serves as an intermediary layer between IoT devices and the cloud backend. It provides real-time metric processing, local analytics, and buffered data transmission to optimize network usage and reduce latency for environmental monitoring systems.

## Features

- **Real-time Metrics Processing**: Receive and process environmental metrics from IoT devices
- **Device Authentication**: Secure API key-based authentication system
- **Local Analytics**: Calculate average consumption and other metrics at the edge
- **Buffered Data Transmission**: Intelligent batching and periodic push to cloud backend
- **RESTful API**: Clean HTTP endpoints for device communication
- **Modular Architecture**: Clean architecture with separated concerns (Domain, Application, Infrastructure, Interfaces)

## Architecture

The project follows a clean architecture pattern with the following modules:

### Analytics Module
- **Domain**: Core business entities (Metric)
- **Application**: Business logic services (MetricService)
- **Infrastructure**: External service integrations and data persistence
- **Interfaces**: REST API endpoints for metric collection

### IAM Module
- **Domain**: Authentication entities (Device) and services
- **Application**: Authentication application services
- **Infrastructure**: Device repository and data storage
- **Interfaces**: Authentication middleware and services

### Shared Module
- **Infrastructure**: Common infrastructure components

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd EcoGuardian-Fog
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

The application uses the following default configurations:

- **API_KEY**: `b1e2c3d4-5f6a-7b8c-9d0e-1f2a3b4c5d6e`
- **DEVICE_ID**: `1`
- **HOST**: `0.0.0.0`
- **PORT**: `9000`
- **BACKEND_URL**: `https://ecoguardian-cgenhdd6dadrgbfz.brazilsouth-01.azurewebsites.net/api/v1/metric-registry`
- **PUSH_INTERVAL**: `120` seconds

## Usage

### Starting the Application

1. Create devices (if needed):
```bash
python create_devices.py
```

2. Start the fog node:
```bash
python app.py
```

The application will start on `http://0.0.0.0:9000` with the following services:
- Device registration
- Periodic metrics push to backend
- REST API for metric collection

### API Endpoints

#### POST /metrics

Submit environmental metrics from IoT devices.

**Headers:**
- `Content-Type: application/json`
- `Api-Key: <device-api-key>`
- `Device-Id: <device-id>`

This is required for proper readings

**Request Body:**
```json
{
  "deviceId": 1,
  "metrics": [
    {
      "metricValue": 25.6,
      "metricTypesId": 1
    },
    {
      "metricValue": 78.3,
      "metricTypesId": 2
    }
  ]
}
```

**Response:**
```json
{
  "report": {
    "4": 45.2
  }
}
```

### Testing

Run the test script to simulate metric submissions:

```bash
python test-metrics.py
```

This will send 10 random metrics to the fog node for testing purposes.

## Metric Types

The system supports different types of environmental metrics:

- **Type 1**: Temperature
- **Type 2**: Humidity  
- **Type 3**: Air Quality
- **Type 4**: Energy Consumption (used for analytics)

## Data Flow

1. **Device Registration**: IoT devices authenticate using API keys
2. **Metric Collection**: Devices send metrics to the fog node via REST API
3. **Local Processing**: Fog node calculates averages and performs edge analytics
4. **Buffering**: Metrics are stored in local buffer for batch processing
5. **Backend Sync**: Periodic push of aggregated data to cloud backend every 2 minutes

## Development

### Project Structure

```
EcoGuardian-Fog/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── create_devices.py      # Device creation utility
├── test-metrics.py        # Testing utility
├── analytics/            # Analytics module
│   ├── application/      # Business logic
│   ├── domain/          # Core entities
│   ├── infrastructure/  # External services
│   └── interfaces/      # REST API
├── iam/                 # Identity and Access Management
│   ├── application/     # Authentication services
│   ├── domain/         # Authentication entities
│   ├── infrastructure/ # Device repository
│   └── interfaces/     # Authentication middleware
└── shared/             # Shared infrastructure
    └── infrastructure/
```

### Key Components

- **Flask Application**: Main web server handling HTTP requests
- **Authentication Service**: Validates device credentials
- **Metric Service**: Processes and analyzes environmental data
- **External Service Facade**: Interfaces with cloud backend
- **Device Repository**: Manages device data and authentication

## Dependencies

- **Flask 3.1.1**: Web framework for REST API
- **Requests 2.32.4**: HTTP client for backend communication
- **Peewee 3.18.1**: ORM for database operations
- **Python-dateutil 2.9.0**: Date/time utilities

## Contributing

1. Follow the clean architecture pattern
2. Write unit tests for new features
3. Ensure proper error handling and logging
4. Document API changes
5. Follow Python PEP 8 style guidelines

## License

This project is part of the EcoGuardian IoT ecosystem for environmental monitoring.

## Support

For issues, questions, or contributions, please contact the development team or create an issue in the project repository.
