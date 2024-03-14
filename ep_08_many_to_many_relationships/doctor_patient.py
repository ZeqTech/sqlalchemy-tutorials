from datetime import datetime

from sqlalchemy import (Column, Date, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = "sqlite:///ep_08_doctor_patient.db"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    appointment_date = Column(Date, default=datetime.utcnow)
    notes = Column(String)

    doctor = relationship("Doctor", backref="appointments")
    patient = relationship("Patient", backref="appointments")

    def __repr__(self):
        return f"<Appointment on {self.appointment_date}>"

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialty = Column(String)

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dob = Column(Date)

Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(Appointment).count() < 1:
    dr_smith = Doctor(name='Dr. Smith', specialty='Cardiology')
    john_doe = Patient(name='John Doe', dob=datetime(1990, 1, 1))
    appointment = Appointment(doctor=dr_smith, patient=john_doe, notes='Routine check-up')

    session.add_all([dr_smith, john_doe, appointment])
    session.commit()

# Find all appointments for Dr. Smith
appointments_for_dr_smith = session.query(Appointment).filter(Appointment.doctor.has(name='Dr. Smith')).all()
print("Dr. Smith's appointments")
print(appointments_for_dr_smith)

# Find all appointments for John Doe
appointments_for_john_doe = session.query(Appointment).filter(Appointment.patient.has(name='John Doe')).all()

print("John Doe's appointments")
print(appointments_for_john_doe)
