from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class AppointmentCreate(BaseModel):
    time_slot: str

class AppointmentOut(BaseModel):
    id: int
    user: str
    time_slot: str
