from pydantic import BaseModel

class CV(BaseModel):
    educationSet: list
    hardskill: list
    softskill: list
    workExperience: list

