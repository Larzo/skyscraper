from bs4 import BeautifulSoup
from lxml import etree as et
from csv import writer
from selenium import webdriver
import chromedriver_binary 
# from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from indeed_job import IndeedJob

class IndeedScraper:
  def __init__(self, search_keyword, location):
    print('in ctor')
    self.search_keyword = search_keyword
    self.location = location
    self.driver = webdriver.Chrome()
    self.jobs = []
    self.job_links = set()

  def __str__(self):
    url = ''
    if hasattr(self,'url'):
      url = self.url
    str = (f'keyword:{self.search_keyword}\n' +
    f'location:{self.location}' +
    url)
    return str

  def save_to_file(self, fname='doc.html'):
    if hasattr(self, 'soup'):
      html_doc = open(fname, 'w')
      html_doc.write(str(self.soup))
    else:
      print('not able to save document')  
  
  def get_jobs(self, start=0):
    paginaton_url = "https://www.indeed.com/jobs?q={}&l={}&radius={}&start={}"

    self.url = paginaton_url.format(self.search_keyword, self.location, 100, start)    
    self.driver.get(self.url)
    content = self.driver.page_source
    self.soup = BeautifulSoup(content, 'html.parser')
    dom = et.HTML(str(self.soup))
    print(f'search keyword {self.search_keyword}')
    try:
      job_list = dom.xpath('//div[@class="job_seen_beacon"]')
      for idx, jb in enumerate(job_list):
        job = IndeedJob(jb, idx)
        self.jobs.append(job)
          
      job_list = self.jobs  
      return(self.jobs)
    except Exception as e:
      pass
    return job_list

  def accumulate(self, attempts=3):
    start = 0
    for i in range(attempts):
      jobs = self.get_jobs(start)
      if len(jobs) == 0:
        print(f'no more jobs at {i}')
        break
      else:
        print(f'{len(jobs)} at {i}')  
      start = len(self.jobs) 
      time.sleep(2)

