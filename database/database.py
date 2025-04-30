from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    company = Column(String, nullable=False)
    salary = Column(Integer, nullable=True)

class Database:
    def __init__(self, db_url="sqlite:///jobs.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def save_jobs(self, jobs):
        session = self.Session()
        try:
            for job in jobs:
                job_entry = Job(**job)
                session.add(job_entry)
            session.commit()
        finally:
            session.close()