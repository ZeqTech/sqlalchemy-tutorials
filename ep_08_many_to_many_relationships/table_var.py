# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# Related Video: https://www.youtube.com/watch?v=iosh_DWnliE

from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = 'sqlite:///ep_08_table_var.db'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Association table
student_course_link = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship(
        'Course', secondary=student_course_link, back_populates='students'
    )


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    students = relationship(
        'Student', secondary=student_course_link, back_populates='courses'
    )


Base.metadata.create_all(engine)

# If there is data in the database, dont add more data
if session.query(Course).count() < 1:
    math = Course(title='Mathematics')
    physics = Course(title='Physics')
    bill = Student(name='Bill', courses=[math, physics])
    rob = Student(name='Rob', courses=[math])

    session.add_all([math, physics, bill, rob])
    session.commit()

rob = session.query(Student).filter_by(name='Rob').first()
courses = [course.title for course in rob.courses]
print(f"Rob's Courses: {', '.join(courses)}")

bill = session.query(Student).filter_by(name='Bill').first()
courses = [course.title for course in bill.courses]
print(f"Bill's Courses: {', '.join(courses)}")
