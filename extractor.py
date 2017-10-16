"""
Requires python Beautiful Soup package:
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
"""

import sys
import csv
from bs4 import BeautifulSoup


file, csv_name = sys.argv[1:]
with open(file) as f:
    html = f.read()
fieldnames = ["Job Title", "Category", "Status", "Location"]
with open(csv_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldnames)
    soup = BeautifulSoup(html, 'html.parser')
    roles = soup.find(attrs={'class': 'roles-results'})
    for row in roles.find_all('tr'):
        tagged_entries = row.find_all(['th', 'td'])
        writer.writerow(entry.get_text(',') for entry in tagged_entries)
