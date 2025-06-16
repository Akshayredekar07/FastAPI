
from pydantic import BaseModel, EmailStr, AnyUrl, field_validator, model_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int 
    weight: float
    married:  bool
    allergies: List[str]
    contact_details: Dict[str, str]


    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        #get correct domain
        domain_name=value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value


    @field_validator('name', mode='after') # mode='after' or mode='before'
    # field validator we can operate it in two model before and after it check the data type in before and after data coercion based on condition 
    @classmethod
    def name_validator(cls, value):
        return value.upper()
    

    @field_validator('age')
    @classmethod
    def age_validator(cls, value):
        if value  > 0 and value < 100:
            return value
        
        else:
            raise ValueError('Age should be in between the 0 and 100')
        
         

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient age more tahn 60 mush have emergency contact')  
        
        return model
    




def get_patient_data(patient: Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.weight)
    print(patient.contact_details)

    print("data fetech successful!")


# Data for patient model class 

# patient_info = {
#     'name': 'nitin', 'email':'abc@hdfc.com' ,'age':30, 'weight':34.5, 'married': True, 'allergies': ['air', 'pollen'], 'contact_details': {'phone':'9545432617'}
# }

patient_info = {
    'name': 'nitin', 'email':'abc@hdfc.com' ,'age':70, 'weight':34.5, 'married': True, 'allergies': ['air', 'pollen'], 'contact_details': {'phone':'9545432617', 'emergency': '453216789'}
}


# object init
patient1 = Patient(**patient_info)  # Validation - type coercion 
# ** is used to unpack the dictniory
get_patient_data(patient1)


# # we can directly pass named argument to the Patient model
# patient2 = Patient(
#     name='nitin',
#     age=30,
#     weight=34.5,
#     married=True,
#     allergies=['pollen', 'dust'],
#     contact_details={'phone': '9999343434'},
#     email='abc@gmail.com',
# )

# get_patient_data(patient=patient2)


