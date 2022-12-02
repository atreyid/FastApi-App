from pydantic import BaseModel, ValidationError, validator

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
        if v < -90 or v > 90:
            raise ValueError('Must lie within -90 to 90')
        return v
    
    @validator('Longitude')
    def l_in_valid_range(cls, v):
        if v < -180 or v > 180:
            raise ValueError('Must lie within -180 to 180')
        return v

    
    
    


    