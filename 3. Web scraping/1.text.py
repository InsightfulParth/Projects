import requests
import pandas as pd
from bs4 import BeautifulSoup

# Send a GET request to the Wikipedia page
url = 'https://en.wikipedia.org/wiki/World_Economic_Forum'
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'lxml')

# Find the table with the title "Overview of past annual meetings"
table = soup.find('table', {'class': 'wikitable'})

# Extract the table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Extract the table rows
rows = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all(['th', 'td'])
    cells = [cell.text.strip() for cell in cells]
    rows.append(cells)

# Create a DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Display the DataFrame
print(df)
