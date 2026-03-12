from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from faker import Faker

fake = Faker()


@dataclass(frozen=True)
class Appointment:
    patient_email: str
    start_time_iso: str
    reason: str


class AppointmentFactory:
    @staticmethod
    def build(*, patient_email: str | None = None) -> Appointment:
        start = datetime.now(tz=timezone.utc) + timedelta(days=3, hours=2)
        return Appointment(
            patient_email=patient_email or fake.unique.email(),
            start_time_iso=start.isoformat(),
            reason=fake.sentence(nb_words=6),
        )

