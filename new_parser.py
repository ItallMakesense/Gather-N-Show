"""
"""

import sys
from pprint import pprint as pprint
import requests


# titles_list = {}
# def parse(data, to_lists):
#     if isinstance(data, dict):
#         for title in data:
#             parse(data[title])
#     elif isinstance(data, list):
#         for element in data:
#             parse(element)

# url = sys.argv[1]
# response = requests.get(url)
# data = response.content.decode()
# transformed_data = json.loads(data)
# pprint(transformed_data)


url = sys.argv[1]
response = requests.get(url)
json_dict = response.json()
pprint(json_dict)
