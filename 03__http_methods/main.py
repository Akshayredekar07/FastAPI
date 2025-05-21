from fastapi import FastAPI
import json

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

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


