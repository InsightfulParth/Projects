#### 1

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
# header
headers = headers[1:4]
# Extract the table rows
rows = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all(['th', 'td'])
    cells = [cell.text.strip() for cell in cells]
    rows.append(cells)

# Create a DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Display the DataFrame
df

#### 2
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Send a GET request to the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Fortune_Global_500'
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'lxml')

# Find the table with the title "Fortune Global 500 list of 2023" (Tag=table & class = wikitable sortable)
table = soup.find('table', {'class': 'wikitable sortable plainrowheaders'})
table
# Extract the table headers
headers = [header.text.strip() for header in table.find_all('th')]

#Extra
headers = headers[1:5]
print((headers))

# Extract the table rows
rows = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    cells = [cell.text.strip() for cell in cells]
    rows.append(cells)

# Create a DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Display the DataFrame
df
