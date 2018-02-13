#add in last_message to db so we can retrieve it upon accidental logout and resume
#if we dont', we will re-post docs we already have in db

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
submit = driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div[2]/div/button')
submit.click()
#sleep(5)
logged_in = False
# while not logged_in:
#     try:
#         user_profile_name = driver.find_element_by_class_name('profile-address').text
#         if user_profile_name == u'zulucapwn':
#             print 'We are logged in'
#             logged_in = True
#     except:
#         print 'Not yet logged in fully'
#         sleep(1)

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


##############
# PRE - LOOP #
##############
soup = BeautifulSoup(driver.page_source, 'lxml')
sleep(2)
scroll_div = soup.find('div', class_='bs-example')
while not scroll_div: #for some reason we don't always get the data
    #print 'Couldn\'t cook the soup'
    soup = BeautifulSoup(driver.page_source, 'lxml')
    sleep(2)
    scroll_div = soup.find('div', class_='bs-example')
#print 'We got soup PRE loop'

#print scroll_div
updates = scroll_div.find_all('p')
#print 'PRE loop updates div is %d long' % len(updates)
last_update = ''
for update in updates:
    #print update
    if 'owned user on' in update.text: #'owned user on'
        #user_link = update.a['href']
        msg = update.text.split(' [Tweet]')[0]
        raw_message = update.text.split(' [Tweet]')[0].split('] ')[1]
        msg_length = len(raw_message) + 1
        #aDict = {'msg':msg}
        hacker = msg.split('] ')[1].split()[0]
        own_level = ' '.join(msg.split('] ')[1].split()[1:4])
        box = msg.split('] ')[1].split()[4]
        aDict = {'hacker': hacker,
                 'own_level': own_level,
                 'box': box,
                 'to_twitter': 0,
                 'to_netsec': 0,
                 'to_netsecfocus': 0,
                 'msg_length': msg_length,
                 'raw_msg': raw_message
                 }
        cursor.insert_one(aDict)
        last_update = msg
        #print 'Last update is now %s' % last_update

    if  'owned system on' in update.text: #'owned system on'
        #user_link = update.a['href']
        msg = update.text.split(' [Tweet]')[0]
        raw_message = update.text.split(' [Tweet]')[0].split('] ')[1]
        msg_length = len(raw_message) + 1
        #aDict = {'msg':msg}
        hacker = msg.split('] ')[1].split()[0]
        own_level = ' '.join(msg.split('] ')[1].split()[1:4])
        box = msg.split('] ')[1].split()[4]
        aDict = {'hacker': hacker,
                 'own_level': own_level,
                 'box': box,
                 'to_twitter': 0,
                 'to_netsec': 0,
                 'to_netsecfocus': 0,
                 'msg_length': msg_length,
                 'raw_msg': raw_message
                 }
        cursor.insert_one(aDict)
        last_update = msg
        #print 'Last update is now %s' % last_update

sleep(5)
update_last = False
########
# LOOP #
########
while 1:

    soup = BeautifulSoup(driver.page_source, 'lxml')
    sleep(2)
    scroll_div = soup.find('div', class_='bs-example')
    while not scroll_div:  # for some reason we don't always get the data
        #print 'Couldn\'t cook the soup in the loop'
        soup = BeautifulSoup(driver.page_source, 'lxml')
        sleep(2)
        scroll_div = soup.find('div', class_='bs-example')
    #print 'We got soup in the loop'

    # print scroll_div
    updates = scroll_div.find_all('p')
    #print 'Looped updates div is %d long' % len(updates)

    try:
        #print 'Beginning try/except'
        for update in reversed(updates):
            update = update.text.split(' [Tweet]')[0]
            #print 'this is the update without .text', update
            #print 'this is the last_update text', last_update
            if update == last_update:
                print 'Latest msg is same as last msg, breaking outta loop'
                break
            else:
                if 'owned user on' in update:  # 'owned user on'
                    raw_message = update.split('] ')[1]
                    # user_link = update.a['href']
                    msg = update
                    msg_length = len(raw_message) + 1
                    # aDict = {'msg':msg}
                    hacker = msg.split('] ')[1].split()[0]
                    own_level = ' '.join(msg.split('] ')[1].split()[1:4])
                    box = msg.split('] ')[1].split()[4]
                    aDict = {'hacker': hacker,
                             'own_level': own_level,
                             'box': box,
                             'to_twitter': 0,
                             'to_netsec': 0,
                             'to_netsecfocus': 0,
                             'msg_length': msg_length,
                             'raw_msg': raw_message
                             }
                    cursor.insert_one(aDict)
                    print 'Inserted to db %s' % msg
                    #last_update = msg
                    update_last = True

                if 'owned system on' in update:  # 'owned system on'
                    raw_message = update.split('] ')[1]
                    # user_link = update.a['href']
                    msg = update
                    msg_length = len(raw_message) + 1
                    # aDict = {'msg':msg}
                    hacker = msg.split('] ')[1].split()[0]
                    own_level = ' '.join(msg.split('] ')[1].split()[1:4])
                    box = msg.split('] ')[1].split()[4]
                    aDict = {'hacker': hacker,
                             'own_level': own_level,
                             'box': box,
                             'to_twitter': 0,
                             'to_netsec': 0,
                             'to_netsecfocus': 0,
                             'msg_length': msg_length,
                             'raw_msg': raw_message
                             }
                    cursor.insert_one(aDict)
                    print 'Inserted to db %s' % msg
                    #last_update = msg
                    update_last = True

        if update_last == True:
            print 'We need to update the last'
            for update in reversed(updates):
                update = update.text.split(' [Tweet]')[0]
                if 'owned user on' in update:  # 'owned user on'
                    last_update = update
                    #last_update = msg
                    update_last = False
                    print 'Updated last is now set to %s' % update
                    break
                if 'owned system on' in update:  # 'owned system on'
                    last_update = update
                    #last_update = msg
                    update_last = False
                    print 'Updated last is now set to %s' % update
                    break

    except:
        print 'Found new Msg\'s but nothing matching owned user or system'

    ##########################
    # READY TO POST TO PROPS #
    ##########################
    ready_to_dump = cursor.find({'to_twitter': 1}).count()
    if ready_to_dump >= 7:
        print 'Ready to post to twitter'
    else:
        print 'we have %d left b4 posting to twitter' %(7 -  ready_to_dump)

    #########
    # SLEEP #
    #########
    print 'Loop done, sleeping 5 mins'
    sleep(60)
    print 'Sleeping 4 mins'
    sleep(60)
    print 'Sleeping 3 min'
    sleep(60)
    print 'Sleeping 2 mins'
    sleep(60)
    print 'Sleeping 1 min'
    sleep(55)
    print 'Executing in 5 secs'
    sleep(5)
    print