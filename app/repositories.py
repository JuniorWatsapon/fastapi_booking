from .entities import User, Appointment

class UserRepository:
    def __init__(self):
        self.users = {
            "admin": User(username="admin", hashed_password="$2b$12$gezv6rHA88KCQ7VBrHmvJu8jFNEtEJ6mmmveDki0r64LLsIf1apMS", is_admin=True), #AdminPass123
            "customer": User(username="customer", hashed_password="$2b$12$RyM3CiB3hmKZD2f5IPGWU.CjXRz3VjRHIbMMCQKSq0Bb8m7q5HpnS", is_admin=False) #CustomerPass123
        }

    def get_by_username(self, username: str):
        return self.users.get(username)

class AppointmentRepository:
    def __init__(self):
        self._appointments = {} # always no appointment for new run
        self._next_id = 1

    def list_all(self):
        return list(self._appointments.values())

    def list_by_user(self, username: str):
        return [a for a in self._appointments.values() if a.user == username]

    def add(self, appointment: Appointment):
        appointment.id = self._next_id
        self._appointments[self._next_id] = appointment
        self._next_id += 1
        return appointment

    def get(self, appointment_id: int):
        return self._appointments.get(appointment_id)

    def delete(self, appointment_id: int):
        if appointment_id in self._appointments:
            del self._appointments[appointment_id]
