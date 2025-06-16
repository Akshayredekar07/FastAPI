
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str = 'Male'
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
    # "gender": "Female",
    "age": 24,
    "address": address1  
}

patient1 = Patient(**patient_dict)

# print(address1)
# print(patient1)



# temp = patient1.model_dump(include={'name', 'address'})
temp = patient1.model_dump(exclude={'address': {'state'}})
temp = patient1.model_dump(exclude_unset=True)
print(temp)
print(type(temp))


# temp1 = patient1.model_dump_json()
# print(temp1)
# print(type(temp1))


