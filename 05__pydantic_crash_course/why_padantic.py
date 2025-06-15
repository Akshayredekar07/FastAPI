

def insert_patient_data(name, age):
    print(name)
    print(age)
    print("Record inserted into database")



# Enhanced function to insert patient data with type and value validation
def insert_data(name: str, age: int):

    if type(name) != str or type(age) != int:
        raise TypeError("Incorrect data type: name must be string, age must be integer")
    
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    print(name)
    print(age)
    print("Record inserted into database")



def update_patient_data(name: str, age: int):
    if type(name) != str or type(age) != int:
        raise TypeError("Incorrect data type: name must be string, age must be integer")
    
    if age < 0:
        raise ValueError("Age cannot be negative")
    
    print(name)
    print(age)
    print("Record updated in database")







if __name__ == "__main__":

    insert_patient_data("nikhil", "thirty")  # Runs without error, but incorrect type

    insert_patient_data("karan", 30)  # Valid input


    

    insert_data("nikhil", 30)  # Valid input

    insert_data("karan", -5)  # Should raise ValueError
    
    # insert_data(123, 25)  # Should raise TypeError


    update_patient_data("arjun", 40)  # Valid input

    update_patient_data("arjun", -10)  # Should raise ValueError





# Notes on validation:
# Need 1: Data type validation
# - Type hints (e.g., name: str, age: int) show expected types to developers.
# - Using type() checks ensures correct types but isn't scalable.
# - Repeating validation in each function (insert_data, update_patient_data) creates duplicate code.
# - In production, manual checks can lead to errors when adding fields like email or new functions.
# - Pydantic (not used here) would centralize validation and reduce repetition.
#
# Need 2: Value validation (e.g., negative age)
# - Added check for age < 0, raising ValueError as requested.
# - Checks for other fields (e.g., email format) would need repetition in every function.
# - This method works but requires manual checks for each field, which is inefficient.
# - Pydantic (not used here) would automatically handle value validation, like ensuring positive age.