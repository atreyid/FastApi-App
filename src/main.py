from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import joblib
import numpy as np
import sys
import os
from pydantic import BaseModel, ValidationError, validator
from typing import List

class House(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @validator('MedInc')
    def med_income_greater_than_zero(cls, v):
        if v <= 0:
            raise ValueError('Must be greater than zero')
        return v

    @validator('HouseAge')
    def house_age_cannot_be_negative(cls,v):
        if v < 0:
            raise ValueError('Must be positive value')
        return v
    
    @validator('AveRooms')
    def average_rooms_cannot_be_negative(cls,v):
        if v < 0:
            raise ValueError('Must be positive value')
        return v

    @validator('AveBedrms')
    def average_bedrms_not_greater_than_ave_rms(cls,v, values, **kwargs):
        if 'AveRooms' in values and v > values['AveRooms']:
            raise ValueError('Average number of bedrooms should be lesser than or equal to average rooms')
        return v


    @validator('Population')
    def population_cannot_be_negative(cls,v):
        if v < 0:
            raise ValueError('Must be positive value')
        return v
    
    @validator('AveOccup')
    def avg_occup_cannot_be_negative(cls,v):
        if v < 0:
            raise ValueError('Must be positive value')
        return v
    
    @validator('Latitude')
    def latitude_in_valid_range(cls, v):
        if v <= -90 or v >= 90:
            raise ValueError('Must lie within -90 to 90')
        return v
    
    @validator('Longitude')
    def longitude_in_valid_range(cls, v):
        if v <= -180 or v >= 180:
            raise ValueError('Must lie within -180 to 180')
        return v

class Houses(BaseModel):
    houses: List[House]

app = FastAPI()

@app.get("/")
def root():
    raise HTTPException(status_code=501,detail="The Endpoint is not implemented")
    
@app.get("/hello")
def hello_name(name:str):
    if not name:
	    # HTTP code 422 is used here because it is the FastAPI's standard for handling invalid contents
        # https://github.com/tiangolo/fastapi/issues/643
        raise HTTPException(status_code=422)    
    return {"message": f"Hello {name}"}

@app.get("/docs")
async def get_docs():
    pass

@app.get("/openapi.json")
def get_json():
    pass

@app.get("/health")
def get_health():
    return datetime.now().isoformat()

@app.post("/predict")
def predict_price(house: House) -> float:
    features = list(house.dict().values())
    script_dir = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(script_dir,'..', 'model_pipeline.pkl')
    loaded_model = joblib.load(model_path)
    y_pred = loaded_model.predict(np.array(features).reshape(1, -1))
    return y_pred[0]
