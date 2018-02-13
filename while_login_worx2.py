#working on making sure we are always logged in and if not, logging in
#in time, this will be added into the log_in script

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from time import sleep
import requests
from pymongo import MongoClient
import htb_sensitive

############
# DATABASE #
############
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.htb #db name
cursor = db.htb #collection name
print htb_sensitive.mongopath


#########
# LOGIN #
#########
driver = webdriver.Chrome('C:\Python27\chromedriver.exe')
driver.get('https://www.hackthebox.eu/home/shoutbox')

email = driver.find_element_by_xpath('//*[@id="email"]')
email.send_keys(htb_sensitive.login_email)
password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys(htb_sensitive.login_password)

#added
remember_me_box = driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div[1]/div/input').click()
remember_me_box_is_checked =  driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div[1]/div/input').is_selected()
#Hack The Box :: Login #login page
try:
    assert driver.title == 'Hack The Box :: Login'
    print 'Yeah'
    logged_in = False
except Exception as e:
    print 'Nope'



submit = driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div[2]/div/button')
submit.click()
#sleep(5)
logged_in = False

while not logged_in:
    try:
        page_title = driver.title
        print page_title
        if page_title == 'Hack The Box :: Shoutbox':
            print 'We are logged in'
            logged_in = True
    except:
        print 'Not yet logged in fully'
        #sleep(1)