import requests
from bs4 import BeautifulSoup


r = requests.Session()
cookies = open('selenium_cookies', 'rb')
for cookie in cookies:
    r.cookies.set(cookie['name'], cookie['value'])
cookies.close()
html = r.get('https://www.hackthebox.eu/home').content
soup = BeautifulSoup(html, 'lxml')
print 'Requests' + str(soup.title)