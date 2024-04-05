

class IndeedJob:
  def __init__(self, job, job_idx):
    self.job_idx = job_idx
    self.job = job

  def get_xml_attr(self, attr):
    xpaths = {
      'company_name': 
        '//div[contains(@class, "company_location")]/div/span[@data-testid="company-name"]/text()',
      'company_location': 
        '//div[contains(@class, "company_location")]/div/div[@data-testid="text-location"]/text()',
      'job_type':
        '//div[contains(@class, "metadata")]/div/text()',
      'salary':
        '/div[contains(@class, "salary-snippet-container")]/div[@data-testid="attribute_snippet_testid"]/text()',
      'apply':
        '//span[@data-testid="indeedApply"]/text()'  
    }
    try:
      result = self.job.xpath(xpaths[attr])[self.job_idx]
    except Exception as e:
      result = 'Not available'
    return result

  def get_job_link(self):
    try:
      job_link = self.job.xpath('./descendant::h2/a/@href')[0]
    except Exception as e:
      job_link = 'Not available'
    return job_link

  def get_job_title(self):
	  try:
	    job_title = self.job.xpath('./descendant::h2/a/span/text()')[0]
	  except Exception as e:
	    job_title = 'Not available'
	  return job_title

  def __str__(self):
    fields = ['job_title', 'company_location', 'company_name', 'job_type']
    str = ''
    for fld in fields:
      str += f'{fld}:{self.fld_val(fld)}\n'
    return str  
    
  def fld_val(self, name: str):
    do = f"get_{name}"
    if hasattr(self, do):
      if callable(func := getattr(self, do)):
        return func()
    else:
      return self.get_xml_attr(name)