from fastapi import FastAPI, Path, HTTPException, Query
import json

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
async def about():
    return {"message": "A fully functional API to manage your patients records."}



@app.get('/view')
async def view():
    return load_data()


@app.get('/patient/{patient_id}/')
def view_patient(patient_id:str = Path(..., description="Id of the patients in DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")




@app.get('/sort')
def sort(sort_by: str = Query(..., description="Sort the patient data based on hieght, weight, bmi"), order:str = Query('asc', description='Sort accoding to asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid filed selected from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Invalid order seleted between asc and desc")
