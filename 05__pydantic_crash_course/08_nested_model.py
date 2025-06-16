from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address






address_dict = {
    "city": "Pune",
    "state": "Maharashtra",
    "pin": "414203"
}

address1 = Address(**address_dict)

patient_dict = {
    "name": "Drishya",
    "gender": "Female",
    "age": 24,
    "address": address1  
}

patient1 = Patient(**patient_dict)

print(address1)
print(patient1)




# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically — no extra work needed