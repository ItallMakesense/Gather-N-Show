"""
Here is your description.
"""

import sys
from pprint import pprint as pprint
import requests


url  = sys.argv[1]
response = requests.get(url)
json_dict = response.json()
jobs = []
if 'count' in json_dict:
    jobs_on_page = len(json_dict['jobs'])
    for page in range(1, json_dict['count']):
        response = requests.get(url, params={'page': page, 'limit': jobs_on_page})
        data = response.json()
        if data['jobs']:
            print("Page number:", page, "| Total jobs number:", len(jobs))
            jobs.extend(data['jobs'])
        else:
            break
else:
    jobs = json_dict
pprint(len(jobs))
