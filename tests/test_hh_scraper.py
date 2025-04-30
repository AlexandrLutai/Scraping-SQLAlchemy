import pytest
from unittest.mock import patch, MagicMock
from scraper.hh_scraper import HH_Scraper

@pytest.fixture
def scraper():
    return HH_Scraper()

@patch('scraper.hh_scraper.requests.get')
def test_fetch_jobs_success(mock_get, scraper):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test HTML</body></html>"
    mock_get.return_value = mock_response

    html = scraper.fetch_jobs(city="moscow", page=0)

    assert html == "<html><body>Test HTML</body></html>"
    mock_get.assert_called_once_with(
        "https://moscow.hh.ru/search/vacancy?page=0",
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )

@patch('scraper.hh_scraper.requests.get')
def test_fetch_jobs_failure(mock_get, scraper):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    html = scraper.fetch_jobs(city="moscow", page=0)

    assert html is None
    mock_get.assert_called_once()

def test_parse_vacancy(scraper):
    html = """
    <div data-qa="vacancy-serp__vacancy">
        <a data-qa="serp-item__title" href="https://example.com">Test Job</a>
        <span data-qa="vacancy-serp__vacancy-employer-text">Test Company</span>
        <span class="magritte-text_typography-label-1-regular___pi3R-_3-0-32">130 000 – 170 000 ₽</span>
    </div>
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    vacancy = soup.find('div', {'data-qa': 'vacancy-serp__vacancy'})

    result = scraper._parse_vacancy(vacancy)

    expected = {
        'title': 'Test Job',
        'link': 'https://example.com',
        'company': 'Test Company',
        'salary': 130000
    }
    assert result == expected

def test_parse_jobs(scraper):
    html = """
    <html>
        <body>
            <div data-qa="vacancy-serp__vacancy">
                <a data-qa="serp-item__title" href="https://example.com">Test Job 1</a>
                <span data-qa="vacancy-serp__vacancy-employer-text">Company 1</span>
                <span class="magritte-text_typography-label-1-regular___pi3R-_3-0-32">100 000 ₽</span>
            </div>
            <div data-qa="vacancy-serp__vacancy">
                <a data-qa="serp-item__title" href="https://example.com/job2">Test Job 2</a>
                <span data-qa="vacancy-serp__vacancy-employer-text">Company 2</span>
                <span class="magritte-text_typography-label-1-regular___pi3R-_3-0-32">200 000 ₽</span>
            </div>
        </body>
    </html>
    """
    jobs = scraper.parse_jobs(html)

    expected = [
        {
            'title': 'Test Job 1',
            'link': 'https://example.com',
            'company': 'Company 1',
            'salary': 100000
        },
        {
            'title': 'Test Job 2',
            'link': 'https://example.com/job2',
            'company': 'Company 2',
            'salary': 200000
        }
    ]
    assert jobs == expected