from __future__ import annotations

from dataclasses import dataclass

from faker import Faker

fake = Faker()


@dataclass(frozen=True)
class Patient:
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: str


class PatientFactory:
    @staticmethod
    def build() -> Patient:
        first = fake.first_name()
        last = fake.last_name()
        return Patient(
            first_name=first,
            last_name=last,
            email=fake.unique.email(),
            phone=fake.msisdn()[:10],
            dob=str(fake.date_of_birth(minimum_age=18, maximum_age=90)),
        )

