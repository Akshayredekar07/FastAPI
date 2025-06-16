
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, AnyUrl

class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title='Name of the patient',
            description='give the name of the patient in less than 50 chars',
            examples=['Nitish', 'Amit']
        )
    ]
    age: int = Field(gt=0, lt=91, description="Age of the patient (1-90)")

    weight: Annotated[float, Field(gt=1, strict=True)]

    married: Annotated[
        Optional[bool],
        Field(default=None, description='Is the patient married or not')
    ]

    allergies: Annotated[
        Optional[list[str]],
        Field(max_length=5, default=None, description="List of allergies (max 5)")
    ]
    
    contact_details: dict[str, str] = Field(description="Contact details of the patient")
    email: EmailStr = Field(description="Email address of the patient")
    linkedin_url: AnyUrl = Field(description="LinkedIn profile URL of the patient")



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.email)
    print(patient.linkedin_url)
    print("inserted")

# object initialization
patient_info = {
    'name': 'nitin',
    'age': 30,
    'weight': 34.5,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '9999343434'},
    'email': 'abc@gmail.com',
    'linkedin_url': 'https://linkedin.com/akshayredekar07'
}

patient1 = Patient(**patient_info)
insert_patient_data(patient=patient1)