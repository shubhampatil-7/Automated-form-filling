import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_automation():
    try:
        # Read the first row of data from CSV
        df = pd.read_csv('data.csv')
        if df.empty:
            return {"status": "error", "message": "No data found in data.csv"}
        
       
        row = df.iloc[0]
        patient_name = row['patient_name']
        date_of_birth = row['date_of_birth']
        claim_amount = str(row['claim_amount'])
        procedure_code = row['procedure_code']

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Get the absolute path of form.html and convert to file URL
        form_path = os.path.abspath("form.html")
        form_url = f"file://{form_path}"

        # Navigate to the form
        driver.get(form_url)
        time.sleep(2)  # Wait for page to load

     
        driver.find_element(By.ID, "name").send_keys(patient_name)
        driver.find_element(By.ID, "dob").send_keys(date_of_birth)
        driver.find_element(By.ID, "claim_amount").send_keys(claim_amount)
        driver.find_element(By.ID, "procedure_code").send_keys(procedure_code)

        # Submit the form
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(2)  # Wait for submission to process

        # Close the driver
        driver.quit()

        return {
            "status": "success",
            "message": f"Form submitted for patient: {patient_name}",
            "data": {
                "patient_name": patient_name,
                "date_of_birth": date_of_birth,
                "claim_amount": claim_amount,
                "procedure_code": procedure_code
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # For testing the automation script directly
    result = run_automation()
    print(result)