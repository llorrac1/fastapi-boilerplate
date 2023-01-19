from pydantic import BaseModel, Field
from typing import Optional



class BaseDto(BaseModel):
    class Config:
        orm_mode = True
