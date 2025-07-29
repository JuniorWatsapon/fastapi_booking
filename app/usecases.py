from .entities import User, Appointment
from .repositories import UserRepository, AppointmentRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user

class AppointmentUseCase:
    def __init__(self, appointment_repo: AppointmentRepository):
        self.appointment_repo = appointment_repo

    def list_appointments(self, user: User):
        if user.is_admin:
            return self.appointment_repo.list_all()
        return self.appointment_repo.list_by_user(user.username)

    def create_appointment(self, user: User, time_slot: str):
        appointment = Appointment(id=0, user=user.username, time_slot=time_slot)
        return self.appointment_repo.add(appointment)

    def delete_appointment(self, user: User, appointment_id: int):
        appt = self.appointment_repo.get(appointment_id)
        if not appt:
            return False
        if not (user.is_admin or appt.user == user.username): #valiadate if admin or username is same so can delete
            return False
        self.appointment_repo.delete(appointment_id)
        return True
