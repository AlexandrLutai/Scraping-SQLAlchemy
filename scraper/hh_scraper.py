import requests
from bs4 import BeautifulSoup
import re

class HH_Scraper:
    
    def fetch_jobs(self, city: str, page=0):
        """
        Получает HTML-код страницы с вакансиями для указанного города.
        """
        url = f"https://{city}.hh.ru/search/vacancy?page={page}"
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка при запросе страницы {url}: {response.status_code}")
            return None

    def _parse_vacancy(self, vacancy):
        """
        Парсит информацию из одного блока вакансии.
        """
        title_tag = vacancy.find('a', {'data-qa': 'serp-item__title'})
        title = title_tag.text.strip() if title_tag else "Не указано"
        link = title_tag['href'] if title_tag else None
        company_tag = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-employer-text'})
        company = company_tag.text.strip() if company_tag else "Не указано"
        salary_tag = vacancy.find('span', {'class': 'magritte-text_typography-label-1-regular___pi3R-_3-0-32'})
        salary = salary_tag.text.strip() if salary_tag else "Не указана"

     
        salary = re.sub(r'[\u202f\xa0]', '', salary)


        match = re.search(r'\d+', salary)
        salary = int(match.group(0)) if match else None

        return {
            'title': title,
            'link': link,
            'company': company,
            'salary': salary
        }

    def parse_jobs(self, html):
        """
        Парсит HTML и извлекает информацию о вакансиях.
        """
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        for vacancy in soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'}):
            job = self._parse_vacancy(vacancy)
            jobs.append(job)
        return jobs


if __name__ == "__main__":
    scraper = HH_Scraper()
    city = "stavropol"  
    html = scraper.fetch_jobs(city=city, page=0)
    if html:
        jobs = scraper.parse_jobs(html)
        print(jobs)
