from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

USER_NAME = 'ilya.kryukov220598@gmail.com'
USER_PASSWOR = 'Ilya22051998'
dictionary = {}

def logins (driver):
    driver.get('https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    email_field = driver.find_element_by_css_selector('#username')
    password_field = driver.find_element_by_css_selector('#password')
    submit_button = driver.find_element_by_css_selector('.btn__primary--large')
    email_field.send_keys(USER_NAME)
    password_field.send_keys(USER_PASSWOR)
    submit_button.click()

def create_driver():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    #chromeOptions.add_argument('headless')
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

def parsing_page(user_id,driver):    
    inf_user={}
    friend_count = driver.find_element_by_xpath("//span[@class='t-16 t-black t-normal']")
    inf_user['friend_count'] = friend_count.text
    photo_link = driver.find_element_by_xpath("//img[@class='pv-top-card__photo presence-entity__image EntityPhoto-circle-9 lazy-image ember-view']")
    inf_user['photo_link'] = photo_link.get_attribute("src")
    common = driver.find_element_by_xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']")
    inf_user['common'] = common.text
    inf_user = user_works(driver,inf_user)
    dictionary[user_id]=inf_user

def user_works(driver,inf_user):
    year_experience = int(0)
    mounth_experience = int(0)

    for work_experience in driver.find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']"):
        split_work_exp = work_experience.text.split(' ')
        if len(split_work_exp)==4:
            year_experience += int(split_work_exp[0])
            mounth_experience += int(split_work_exp[2])
        elif len(split_work_exp) == 2:
            if split_work_exp[1]=='г.':
                year_experience += int(split_work_exp[0])
            else:
                mounth_experience += int(split_work_exp[0])

    if mounth_experience > 12:
        year_experience += int(int(mounth_experience)//12)
        mounth_experience -= int((int(mounth_experience)//12)*12)

    inf_user['work_experience'] = str(year_experience) + " г. "+ str(mounth_experience) + " мес."         
       
    return inf_user

def user_education(driver,inf_user):





def start_search(driver):
    with open('input.txt','r') as input:
        for n, user_id in enumerate(input, 1):
            user_id = user_id.rstrip('\n')
            driver.get('https://www.linkedin.com/in/'+user_id+'/')
            parsing_page(user_id,driver)


driver = create_driver()
logins(driver)
start_search(driver)

