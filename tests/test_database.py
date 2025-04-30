import pytest
from database.database import Database, Job

@pytest.fixture
def test_db():
    """
    Фикстура для создания временной базы данных в памяти.
    """
    db = Database(db_url="sqlite:///:memory:")  #
    return db

def test_create_tables(test_db):
    """
    Тест создания таблиц.
    """
    inspector = test_db.engine.dialect.get_table_names(test_db.engine)
    assert "jobs" in inspector

def test_save_jobs(test_db):
    """
    Тест сохранения вакансий в базу данных.
    """
    jobs = [
        {"title": "Python Developer", "link": "https://example.com", "company": "Example Inc.", "salary": 100000},
        {"title": "Data Scientist", "link": "https://example.com/job2", "company": "Data Corp.", "salary": 120000},
    ]

    test_db.save_jobs(jobs)

    session = test_db.Session()
    try:
        saved_jobs = session.query(Job).all()
        assert len(saved_jobs) == 2
        assert saved_jobs[0].title == "Python Developer"
        assert saved_jobs[1].title == "Data Scientist"
    finally:
        session.close()

def test_get_jobs(test_db):
    """
    Тест извлечения вакансий из базы данных.
    """
    jobs = [
        {"title": "Python Developer", "link": "https://example.com", "company": "Example Inc.", "salary": 100000},
        {"title": "Data Scientist", "link": "https://example.com/job2", "company": "Data Corp.", "salary": 120000},
    ]

    test_db.save_jobs(jobs)

    session = test_db.Session()
    try:
        saved_jobs = session.query(Job).all()
        assert len(saved_jobs) == 2
        assert saved_jobs[0].title == "Python Developer"
        assert saved_jobs[0].salary == 100000
        assert saved_jobs[1].company == "Data Corp."
    finally:
        session.close()