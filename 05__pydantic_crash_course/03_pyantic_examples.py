
from pydantic import BaseModel


class Patient(BaseModel):
    name:str
    age:int



def insert_patient_data(name, age):

    patient_info = {'name': 'nitin', 'age':30}

    patient1 = Patient(**patient_info)

