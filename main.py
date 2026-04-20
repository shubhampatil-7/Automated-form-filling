from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from automation import run_automation
from fhirpy import SyncFHIRClient
import os
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI(title="Healthcare RPA API", description="A healthcare automation tool with RPA, FastAPI, Docker, and FHIR integration")

# Initialize FHIR client (using public test server)
fhir_client = SyncFHIRClient(os.getenv("FHIR_SERVER_URL", "https://hapi.fhir.org/baseR4"))

@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Healthcare RPA API is running"}

@app.post("/run-automation", tags=["Automation"])
async def run_automation_endpoint():
    """Trigger the Selenium automation script"""
    try:
        result = run_automation()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patient/{patient_id}", tags=["FHIR"])
async def get_patient(patient_id: str):
    """Fetch a patient from the FHIR server"""
    try:
        patient = fhir_client.resources('Patient').search(_id=patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
        # Return the patient as a dictionary (serialize the FHIR resource)
        return patient.serialize()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)