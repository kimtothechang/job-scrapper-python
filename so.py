import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}


def get_last_page():
    result = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page = pages[-2].get_text(strip=True)

    return int(last_page)


def extract_job(html):
    title = html.find('h2', {'class': 'mb4'}).find('a').string
    try:
      company = html.find('h3', {'class': 'mb4'}).find('span').string.strip()
    except AttributeError:
      company = html.find('h3', {'class': 'mb4'}).find('span').string
    location = html.find('h3', {
        'class': 'mb4'
    }).find('span', {
        'class': 'fc-black-500'
    }).string.strip()
    job_id = html['data-jobid']

    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping SO Page: {page}')
        result = requests.get(f"{URL}&pg={page+1}", headers=HEADERS)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
