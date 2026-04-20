# Healthcare RPA Automation Tool

A Python-based healthcare automation tool that combines Robotic Process Automation (RPA) with a RESTful API to automate healthcare claim form submissions. The tool uses Selenium for browser automation and API to provide a clean interface for triggering automation workflows and fetching patient data from FHIR servers.

## How It Works

The system operates in two main modes:

1. **RPA Automation Mode**: When triggered via the `/run-automation` endpoint, the system:
   - Reads patient data from `data.csv`
   - Launches a headless Chrome browser using Selenium
   - Loads a healthcare claim form (`form.html`)
   - Automatically fills the form with patient data
   - Submits the form
   - Returns success/failure status

2. **FHIR Integration Mode**: When querying the `/patient/{patient_id}` endpoint, the system:
   - Sends a request to the public FHIR test server (https://hapi.fhir.org/baseR4)
   - Retrieves and returns patient data in JSON format
   - Enables easy patient lookup for automation workflows

## Features

- **RPA Automation**: Uses Selenium to automate filling and submitting a healthcare claim form with real patient data
- **FastAPI**: Provides RESTful endpoints to trigger automation workflows and fetch patient data
- **Dockerized**: Easy deployment with Docker and docker-compose for consistent environments
- **FHIR Integration**: Fetches patient data from a public FHIR server (HAPI FHIR) for realistic data handling
- **Healthcare Focus**: Designed specifically for healthcare data automation scenarios (note: not HIPAA compliant for production use)
- **Interactive Documentation**: Automatic Swagger UI generation for easy API exploration

## Project Structure

- `automation.py`: Selenium script to automate form filling.
- `data.csv`: Sample patient data for the automation.
- `form.html`: Simple HTML form used by the automation script.
- `main.py`: FastAPI application with endpoints.
- `Dockerfile`: Docker configuration.
- `docker-compose.yml`: Docker-compose for easy startup.
- `requirements.txt`: Python dependencies.

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- Git (to clone the repository)

### Local Deployment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd healthcare-rpa-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`.

### Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`.

2. Alternatively, build and run the Docker image directly:
   ```bash
   docker build -t healthcare-rpa-api .
   docker run -p 8000:8000 healthcare-rpa-api
   ```

## API Endpoints

- `GET /`: Health check endpoint.
- `POST /run-automation`: Triggers the Selenium automation script to fill and submit the form with the first row of data from `data.csv`.
- `GET /patient/{patient_id}`: Fetches a patient from the public FHIR server (https://hapi.fhir.org/baseR4) by ID.

## Testing the API

### Using curl

1. Health check:
   ```bash
   curl http://localhost:8000/
   ```

2. Run automation:
   ```bash
   curl -X POST http://localhost:8000/run-automation
   ```

3. Get patient (replace `123` with an actual patient ID from the FHIR server):
   ```bash
   curl http://localhost:8000/patient/123
   ```

### Using Swagger UI

Once the application is running, visit `http://localhost:8000/docs` to see the interactive API documentation.

## Notes

- **HIPAA Compliance**: This project is for demonstration purposes only. In a production environment, additional security, privacy, and compliance measures (such as encryption, access controls, audit logs, etc.) would be required to handle protected health information (PHI) in accordance with HIPAA regulations.
- **FHIR Server**: The application uses the public FHIR test server at https://hapi.fhir.org/baseR4. For production, you would replace this with a secure, compliant FHIR server.
- **Selenium**: The automation script uses a headless Chrome browser. In a production setting, you might want to use a more robust RPA platform or attend to browser dependencies and security.

## License

This project is open source and available under the [MIT License](LICENSE).
