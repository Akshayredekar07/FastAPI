

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int 
    weight: float
    height: float
    married:  bool
    allergies: List[str]
    contact_details: Dict[str, str]


    @computed_field
    def bmi(self) -> float:
        # BMI = weight (kg) / [height (m)]²
        bmi = round((self.weight/(self.height**2)), 2)

        return bmi
        


def get_patient_data(patient: Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.weight)
    print(patient.contact_details)
    print("BMI", patient.bmi)

    print("data fetech successful!")


# Data for patient model class 


patient_info = {
    'name': 'nitin', 'email':'abc@hdfc.com' ,'age':70, 'weight':34.5, 'married': True, 'allergies': ['air', 'pollen'], 'contact_details': {'phone':'9545432617', 'emergency': '453216789'}
}


# object init
patient1 = Patient(**patient_info)  
get_patient_data(patient1)


