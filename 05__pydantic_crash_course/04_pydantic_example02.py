

from pydantic import BaseModel
from typing import List
from typing import Dict
from typing import Optional

from pydantic import EmailStr
from pydantic import AnyUrl


class Patient(BaseModel):
    name:str
    age:int
    weight:float
    # married:bool
    # allergies: list[str]
    allergies: Optional[list[str]] = None
    contact_details: dict[str, str]
    
    # To make ths field optional by default all fields defined in the pydantic model class we have to provie the data for this but we can also use the optional

    # we can also set default values for the fields
    married: bool = False

    email: EmailStr
    linkedin_url: AnyUrl




def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print("inserted")


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print("updated")


    
# object initilization
    
# patient_info = {'name': 'nitin', 'age':30}
# patient_info = {'name': 'nitin', 'age':'thirty'}
# patient_info = {'name': 'nitin', 'age':30, 'weight': 34.5, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'email':'abc@gmail.com', 'phone':'9999343434'}}


# patient_info = {'name': 'nitin', 'age':30, 'weight': 34.5, 'married': True,  # 'allergies': ['pollen', 'dust'], 
# 'contact_details':{'email':'abc@gmail.com', 'phone':'9999343434'}}


# patient_info = {'name': 'nitin', 'age':30, 'weight': 34.5, 
# 'married': True,  # 'allergies': ['pollen', 'dust'], 
# 'contact_details':{'email':'abc@gmail.com', 'phone':'9999343434'}}


patient_info = {'name': 'nitin', 'age':30, 'weight': 34.5, 
# 'married': True,  # 'allergies': ['pollen', 'dust'], 
'contact_details':{'phone':'9999343434'},
'email':'abc@gmail.com', 
'linkedin_url': 'https://linkedin.com/akshayredekar07'
}

patient1 = Patient(**patient_info)

# call the function
insert_patient_data(patient=patient1)