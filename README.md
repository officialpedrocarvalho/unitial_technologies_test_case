
# Data Analyzer - Django Application

## Description

This tool is designed to analyze data from machines used during a weekly work cycle. It ingests data logged on the machines, calculates key insights, and returns useful information about their usage. The tool exposes a REST API that processes JSON data to answer several questions regarding the machines' activity and consumption.

The core functionality includes calculating the average start and end times, total working hours, and the amount of fuel or energy consumed by each machine. Additionally, the tool identifies the day with the highest consumption (either diesel or electricity) and can provide other relevant insights from the data.

The application is built using Python and is capable of running locally or being deployed in a cloud environment.

## Features

- **Register Machines on the system**: Registers new machines on the system
- **Average Start and End Time**: Calculates the average start and end times of each machine's work for the week.
- **Total Hours Worked**: Computes the total number of hours worked by each machine during the week.
- **Fuel/Power Consumption**: Determines the amount of diesel (L) or electricity (kWh) consumed by each machine based on the logged fuel levels.
- **Highest Consumption Day**: Identifies the day with the highest diesel and electricity consumption.

---

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.9 or higher
- Docker (optional, if using Docker Compose)
- Docker Compose (optional, if using Docker Compose)

---

## Setup Instructions

### Using Docker

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the Docker image based on the `Dockerfile`.
   - Set up the Django app inside a container.

3. Access the application at `http://localhost:8000`.

4. To stop the containers:
   ```bash
   docker-compose stop
   ```

---

### Without Docker

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   .\venv\Scripts\activate   # For Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. The application will be accessible at `http://localhost:8000`.

---

## Running Migrations

Once the application is set up, you will need to run migrations to initialize the database:

1. Using Docker, run the following command inside the container:
   ```bash
   docker-compose exec data_analyzer python manage.py migrate
   ```

2. Without Docker, simply run:
   ```bash
   python manage.py migrate
   ```

This will apply the necessary database migrations for the application.

---

## Testing

To test the application’s functionality:

1. With Docker:
   ```bash
   docker-compose exec data_analyzer python manage.py test
   ```

2. Without Docker:
   ```bash
   python manage.py test
   ```

This will run the tests that are included in the app.

---

## API Requests and Examples

Here are the details on how to interact with the API endpoints of the **Data Analyzer Tool**.

---

### 1. **Register New Machines**

This endpoint allows you to register new machines by sending a JSON payload that matches the `machines.json` format.

**Endpoint:** `POST /api/machine/`

**Request:**

To register new machines, you can send a `POST` request with the following JSON body:

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json"      -d @machines.json      http://localhost:8000/api/machine/
```

**Request Body:**

```json
[
  {
    "id": "9174277a",
    "manufacturer": "Caterpillar",
    "type": "excavator",
    "fuel_type": "electric",
    "battery_size": 115
  },
  {
    "id": "8645afde",
    "manufacturer": "Volvo",
    "type": "forklift",
    "fuel_type": "diesel",
    "fuel_tank_size": 49
  }
]
```

**Response:**

A successful response will confirm that the machines have been registered.

```json
{
  "message": "Machines registered successfully!"
}
```

**HTTP Status Code:** 201 Created

---

### 2. **Get Machine Analysis**

This endpoint processes the data of the machines, such as their working hours and fuel consumption, and returns the analysis results.

**Endpoint:** `GET /api/machine/analysis/`

**Request:**

Send a `GET` request with the data (matching the `data.json` format) to analyze the machines' performance.

**Example using `curl`:**

```bash
curl -X GET -H "Content-Type: application/json"      -d @data.json      http://localhost:8000/api/machine/analysis/
```

**Request Body:**

```json
 [
  {
    "timestamp": 1683199625071,
    "machine_id": "ab13141f",
    "battery_SoC": 0.6162345415
  },
  {
    "timestamp": 1682946296977,
    "machine_id": "38de4d48",
    "fuel_level": 0.4148975679
  }
]
```

**Response:**

The analysis result will include details like machine IDs, average start/end times, total hours worked, and fuel consumed.

```json
[
  {
    "machine_id": "ab13141f",
    "average_start": "07:15:00",
    "average_end": "16:18:49",
    "hours_worked": 40,
    "fuel_consumed": "120.55 kWh"
  },
  {
    "machine_id": "38de4d48",
    "average_start": "06:44:17",
    "average_end": "16:39:32",
    "hours_worked": 35,
    "fuel_consumed": "305.60 L"
  }
]
```

**HTTP Status Code:** 200 OK

---

### 3. **Get the Day with the Highest Consumption**

This endpoint calculates which day had the highest fuel or energy consumption based on the provided machine data.

**Endpoint:** `GET /api/machine/highest_consumption_day/`

**Request:**

Send a `GET` request with the `data.json` that contains the necessary logs.

**Example using `curl`:**

```bash
curl -X GET -H "Content-Type: application/json"      -d @data.json      http://localhost:8000/api/machine/highest_consumption_day/
```

**Request Body:**

```json

[
  {
    "timestamp": 1683199625071,
    "machine_id": "ab13141f",
    "battery_SoC": 0.6162345415
  },
  {
    "timestamp": 1682946296977,
    "machine_id": "38de4d48",
    "fuel_level": 0.4148975679
  }
]

```

**Response:**

The response will provide the day with the highest consumption.

```json
{
  "day": "2025-01-10",
  "diesel_consumption": "42 L",
  "electricity_consumption": "56 kWh"
}
```

**HTTP Status Code:** 200 OK

---

### General Notes:

- **Machine Registration**: You need to register machines first with the `POST /api/machine` endpoint. After registration, you can run data analysis or get consumption details for these machines.
- **Analysis and Consumption**: Once the machines are registered, you can analyze the machine data using the `GET /api/machine/analyzes` and `GET /api/machine/highest_consumption_day` endpoints to gather insights like total fuel consumption and the day with the highest consumption.
- **Consumption**: The endpoint has been created, but the implementation is pending as it requires more time.
- **Tests**: I’ve added unit tests for a few scenarios of one method as an example, to avoid spending excessive time on writing tests for all methods and cases. Integration tests are also needed to validate the API endpoints.

---