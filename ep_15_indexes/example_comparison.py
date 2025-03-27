# =============================================================
# |                 Created By: ZeqTech                       |
# |         YouTube: https://www.youtube.com/@zeqtech         |
# =============================================================
# https://www.youtube.com/watch?v=WsDVBEmTlaI

# This file will show you a comparison of having vs not having an index
# and how it affects reading data and writing data from a database


from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, String, Sequence
import time

# Set up the SQLite database
engine = create_engine('sqlite:///example.db', echo=False)

# Optional set to memory instead of a file
# engine = create_engine('sqlite:///:memory:', echo=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Sequence('id_seq'), primary_key=True)


class WithoutIndex(Base):
    __tablename__ = 'without_index'
    data: Mapped[str] = mapped_column(String(50))


class WithIndex(Base):
    __tablename__ = 'with_index'
    data: Mapped[str] = mapped_column(String(50), index=True)


# Database connection
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

# Create session
s = sessionmaker(bind=engine)
session: Session = s()


# Function to insert data into a table
def insert_data(session: Session, model: WithoutIndex | WithIndex, num_rows: int):
    start_time = time.perf_counter()
    models = []
    for i in range(num_rows):
        if i % 10_000 == 0:
            print(f'\r{i:>10,} / {num_rows:,}', end='\r')
            session.bulk_save_objects(models)
            models = []

        models.append(model(data=f'data_{i}'))

    session.bulk_save_objects(models)
    session.commit()
    end_time = time.perf_counter()
    return round(end_time - start_time, 4)


def fetch_data(session: Session, model: WithoutIndex | WithIndex):
    start_time = time.perf_counter()
    data = session.query(model).filter(model.data == 'data_5343').first()
    end_time = time.perf_counter()
    return round(end_time - start_time, 4)


def calc_time(start, end):
    value = round((end - start) / start, 2) * 100
    return abs(value)


# =============================================================
#                       INSERTING DATA
# =============================================================
# Insert data into table without index
num_rows = 500_000
print(f'Writing Data - {num_rows:,} rows without an index')
time_without_index = insert_data(session, WithoutIndex, num_rows)
print(
    f'Time to insert {num_rows:,} rows without index: {time_without_index:,} seconds\n'
)

# Insert data into table with index
print(f'Writing Data - {num_rows:,} rows with an index')
time_with_index = insert_data(session, WithIndex, num_rows)
print(f'Time to insert {num_rows:,} rows with index: {time_with_index:,} seconds\n')

diff = calc_time(time_without_index, time_with_index)
print(f'Adding index increased inserting data time by: {diff:.2f}% 😱😱\n\n')


# =============================================================
#                       QUERYING DATA
# =============================================================
print('Reading Data')
num_rows = session.query(WithoutIndex).count()
time_without_index = fetch_data(session, WithoutIndex)
print(f'Time to query {num_rows:,} rows without index: {time_without_index:,} seconds')

num_rows = session.query(WithIndex).count()
time_with_index = fetch_data(session, WithIndex)
print(f'Time to query {num_rows:,} rows with index: {time_with_index:,} seconds')

diff = calc_time(time_without_index, time_with_index)
print(f'Adding index sped up query by: {diff:.2f}% 🎉🎉\n\n')


# =============================================================
#                       CLEAN UP SESSION
# =============================================================
session.close()
