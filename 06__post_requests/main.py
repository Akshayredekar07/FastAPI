from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal



class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Id of the patient", examples=['P001'])]
    name:Annotated[str, Field(..., description="Name of the patient")]
    city:Annotated[str, Field(..., description="Where thr Patient leaving")]
    age:Annotated[int , Field(..., gt=1, lt=100, description="Age of the patient")]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="gGender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meter")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Mormal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        




def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)



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



@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()
    # Check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude={'id'})

    # save the data into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'messge': "Patient created successful"})




