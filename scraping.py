from bs4 import BeautifulSoup
import requests

url = 'https://github.com/MaiMouri'

res = requests.get(url)  # <Response [200]>
soup = BeautifulSoup(res.text, 'html.parser')

follower = soup.find('span', {'class': 'text-bold color-fg-default'}).text
# print(soup.find_all('a', {'class': 'Link--secondary no-underline no-wrap'}))
print(follower)
