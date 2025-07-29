from pydantic import BaseModel

class User(BaseModel):
    username: str
    hashed_password: str
    is_admin: bool = False

class Appointment(BaseModel):
    id: int
    user: str
    time_slot: str
