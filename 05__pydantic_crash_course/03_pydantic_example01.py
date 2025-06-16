
from pydantic import BaseModel


class Patient(BaseModel):
    name:str
    age:int



def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("inserted")


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("updated")


    
# object initilization
    
patient_info = {'name': 'nitin', 'age':30}
# patient_info = {'name': 'nitin', 'age':'thirty'}

patient1 = Patient(**patient_info)

# call the function
insert_patient_data(patient=patient1)