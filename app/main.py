from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from app.dependencies import get_current_user
from app.usecases import AuthUseCase, AppointmentUseCase
from app.repositories import UserRepository, AppointmentRepository
from app.auth import create_access_token
from app.schemas import Token, AppointmentCreate, AppointmentOut

app = FastAPI()

user_repo = UserRepository()
appointment_repo = AppointmentRepository()
auth_uc = AuthUseCase(user_repo)
appointment_uc = AppointmentUseCase(appointment_repo)

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_uc.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/appointments/", response_model=List[AppointmentOut])
async def list_appointments(current_user = Depends(get_current_user)):
    return appointment_uc.list_appointments(current_user)

@app.post("/appointments/", response_model=AppointmentOut, status_code=201)
async def create_appointment(appointment: AppointmentCreate, current_user = Depends(get_current_user)):
    return appointment_uc.create_appointment(current_user, appointment.time_slot)

@app.delete("/appointments/{appointment_id}", status_code=204)
async def delete_appointment(appointment_id: int, current_user = Depends(get_current_user)):
    success = appointment_uc.delete_appointment(current_user, appointment_id)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized or appointment not found")
    return
