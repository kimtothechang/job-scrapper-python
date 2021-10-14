import requests
from bs4 import BeautifulSoup

LIMIT = 10
URL = "https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C&l=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("ul", {"class": "pagination-list"})

    links = pagination.find_all('li')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {
        "class": "jobTitle"
    }).find('span', title=True).text
    try:
      company = html.find("span", {"class": "companyName"}).text
    except AttributeError:
      company = 'no_compnay_name'
    location = html.find("div", {"class": "companyLocation"}).text
    job_id = html["data-jk"]
    
    return {'title': title, 'company': company, 'location': location,'link':f"https://kr.indeed.com/viewjob?jk={job_id}&tk=1fhq95u1o379b000&from=serp&vjs=3"}


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    if page == 0:
      result = requests.get(URL)
    else:
      result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "resultWithShelf"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs



def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  
  return jobs