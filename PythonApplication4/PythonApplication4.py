from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time 
from pprint import pformat
import sys
import json


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
    chromeOptions.add_argument('headless')
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

def parsing_page(user_id,driver):     
    inf_user={}
    time.sleep(1)

    try:
        friend_count = driver.find_element_by_xpath("//span[@class='align-self-center t-14 t-black--light']")
        inf_user['friend_count'] = friend_count.text
    except NoSuchElementException:
        inf_user['friend_count'] = "none"    
   
    photo_link = driver.find_element_by_xpath("//img[@class='pv-top-card__photo presence-entity__image EntityPhoto-circle-9 lazy-image ember-view']")
    inf_user['photo_link'] = photo_link.get_attribute("src")    
    inf_user['common'] = user_common (driver)
    load_hidden_blocks (driver)
    inf_user['work_experience'] = user_works_experience(driver)
    inf_user['education'] = user_education (driver)
    inf_user['works'] = user_works(driver)
    inf_user['skills'] = user_skills(driver)
    inf_user['interests'] = user_interests(driver)
    dictionary[user_id]=inf_user

def load_work_block(driver):
    try:
        block_works = driver.find_element_by_xpath("//section[@id='experience-section']")
        actions = ActionChains(driver)
        actions.move_to_element(block_works).perform()
                
        try:
            while 1 :
                button_see_more = block_works.find_element_by_xpath(".//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link-without-visited-state']")        
                actions.move_to_element(button_see_more).perform()
                button_see_more.click()
        except : NoSuchElementException
    except : NoSuchElementException

def load_education_block(driver):
    try:
        block_education = driver.find_element_by_xpath("//section[@id='education-section']")
        actions = ActionChains(driver)
        actions.move_to_element(block_education).perform()
        
        try:
            while 1 :
                button_see_more = block_education.find_element_by_xpath(".//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link-without-visited-state']")
                actions.move_to_element(button_see_more).perform()
                button_see_more.click()
        except : NoSuchElementException
    except:NoSuchElementException

def load_skills_block(driver):
    try:
        block_skills = driver.find_element_by_xpath("//section[@class='pv-profile-section pv-skill-categories-section artdeco-container-card artdeco-card ember-view']")
        actions = ActionChains(driver)
        actions.move_to_element(block_skills).perform()

        button_see_more = block_skills.find_element_by_xpath(".//button[@data-control-name='skill_details']")
        actions.move_to_element(button_see_more).perform()
        button_see_more.click()        
    except : NoSuchElementException

def load_hidden_blocks (driver):
    actions = ActionChains(driver)
    for hidden_block in driver.find_elements_by_xpath("//div[@class='pv-deferred-area pv-deferred-area--pending pv-deferred-area--occluded ember-view']"):
        actions.move_to_element(hidden_block).perform()
    time.sleep(1)

def user_common (driver):
    try:        
        block_common = driver.find_element_by_xpath("//section[@class='artdeco-container-card pv-profile-section pv-about-section artdeco-card ember-view']")
        if block_common.text == "":
            return "none"
        actions = ActionChains(driver)        
        actions.move_to_element(block_common).perform()        
        text_common = block_common.text
        return text_common

    except NoSuchElementException:
        return "none"

     
def user_works_experience(driver):   

    load_work_block(driver)
    actions = ActionChains(driver)        
        

    try:
        block_works = driver.find_element_by_xpath("//section[@id='experience-section']") 
        actions.move_to_element(block_works.find_element_by_xpath(".//header")).perform() 
    except NoSuchElementException:
        return "none"

    year_experience = int(0)
    mounth_experience = int(0)
    
    work_experience_years = block_works.find_elements_by_xpath(".//h4[@class='pv-entity__date-range t-14 t-black--light t-normal']//span[2]")
    work_experience = block_works.find_elements_by_xpath(".//span[@class='pv-entity__bullet-item-v2']")

    max_now_work_experience=[]
    end_year=int(2020)

    for i in range(0, len(work_experience)):
        actions.move_to_element(work_experience[i]).perform()
        if "настоящее время" in work_experience_years[i].text:

            try:
                year_start_work = int( work_experience_years[i].text.split(' ')[1])
            except Exception:
                year_start_work = int( work_experience_years[i].text.split(' ')[0])
            if end_year > int(year_start_work):
                end_year = int(year_start_work)

            split_work_exp = work_experience[i].text.split(' ')
            if len(split_work_exp)==4:
                max_now_work_experience.append(float(str(split_work_exp[0])+"."+str(split_work_exp[2])))
            elif len(split_work_exp) == 2:
                if split_work_exp[1] in ['г.','лет']:
                    max_now_work_experience.append(float(split_work_exp[0]+"."+str(0)))
                else:
                    max_now_work_experience.append(float(str(0)+"."+str(split_work_exp[0])))
        else:
            split_work_exp = work_experience[i].text.split(' ')
            if len(split_work_exp)==4:
                year_experience += int(split_work_exp[0])
                mounth_experience += int(split_work_exp[2])
            elif len(split_work_exp) == 2:
                if split_work_exp[1] in ['г.','лет']:
                    year_experience += int(split_work_exp[0])
                else:
                    mounth_experience += int(split_work_exp[0])
            try:
                work_experience_years_split = work_experience_years[i].text.split(' ')
                year_start_work= work_experience_years_split[1]
                year_end_work = work_experience_years_split[len(work_experience_years_split)-2]

                if int(year_end_work) > int(end_year):
                    year_experience -= (int(year_end_work)-int(end_year))
                if end_year > int(year_start_work):
                    end_year = int(year_start_work)
            except: Exception
    try:
        max_now_work = max(max_now_work_experience)
        max_now_work_split = str(max_now_work).split('.')        
        year_experience += int(max_now_work_split[0])
        mounth_experience += int(max_now_work_split[1]) 
    except: Exception

    if mounth_experience > 12:
        year_experience += int(int(mounth_experience)//12)
        mounth_experience -= int((int(mounth_experience)//12)*12)

    experience = str(year_experience) + " г. "+ str(mounth_experience) + " мес."         
       
    return experience

def user_education(driver):    

    load_education_block(driver)
    try:
        block_education = driver.find_element_by_xpath("//section[@id='education-section']")
    except NoSuchElementException:
        return "none"
    educations = {}
    for inf_place in block_education.find_elements_by_xpath(".//li[@class='pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view']"):
        inf_place_split = inf_place.text.split('\n')
        place = {}
        place['type'] = 'University'
        try:
            dates = inf_place_split[6].split('–')        
            place['dt_start'] = str(dates[0])
            place['dt_end'] = str(dates[1])
        except IndexError:
            place['dt_start'] = 'none'
            place['dt_end'] = 'none'
        place['name'] = str( inf_place_split[0])
        try:
            place['description'] = str(inf_place_split[2]+", "+inf_place_split[4])
        except IndexError:
            place['description'] = 'none'
        
        educations[str(inf_place_split[0])]=place
    
    return educations

def user_works(driver):

    works = {}

    load_work_block(driver)
    try:
        block_works = driver.find_element_by_xpath("//section[@id='experience-section']")  
    except NoSuchElementException:
        return "none"

    actions = ActionChains(driver)    

    for inf_work in block_works.find_elements_by_xpath(".//li[@class='pv-entity__position-group-pager pv-profile-section__list-item ember-view']"):
        try:
            inf_work_split = inf_work.text.split('\n')
            work = {}   
        
            try:
                dates = inf_work_split[4].split('–')        
                work['dt_start'] = dates[0]
                work['dt_end'] = dates[1].replace(" ","",1)
            except IndexError:
                work['dt_start'] = 'none'
                work['dt_end'] = 'none'

            work_name = inf_work_split[2]
            try:
                working_day=inf_work.find_element_by_xpath(".//span[@class='pv-entity__secondary-title separator']")
                work_name = work_name.replace(str(working_day.text),'')
            except: NoSuchElementException

            work['name'] = work_name
            try:
                work['description'] = inf_work_split[0]
            except IndexError:
                work['description'] = 'none'
        
            works[work_name]=work 
        except : Exception
    
    return works


def user_skills (driver):

    load_skills_block(driver)  
    
    try:
        block_skills = driver.find_element_by_xpath("//section[@class='pv-profile-section pv-skill-categories-section artdeco-container-card artdeco-card ember-view']")
    except NoSuchElementException:
        return "none"

    skills =[]
    for user_skill in block_skills.find_elements_by_xpath("//span[@class='pv-skill-category-entity__name-text t-16 t-black t-bold']"):
        try:
            skills.append("name: "+str(user_skill.text))
        except: NoSuchElementException
    return skills

def user_interests(driver):
    interests = []

    try:
        block_interests = driver.find_element_by_xpath("//section[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']")
    except NoSuchElementException:
        return "none"

    try:
        see_more = driver.find_element_by_xpath("//a[@data-control-name='view_interest_details']")
        actions = ActionChains(driver)
        actions.move_to_element(see_more).perform()
        see_more.click()
        time.sleep(2)
        interests_page = driver.find_element_by_xpath("//nav[@class='pv-profile-detail__nav ember-view']")                
        for button_innterest_page in interests_page.find_elements_by_tag_name('a'):
            button_innterest_page.click()
            time.sleep(1)            
            interests_page_content = driver.find_element_by_xpath("//div[@class='entity-list-wrapper ember-view']")
            count_interests_in_page = len(interests_page_content.find_elements_by_tag_name('li'))
            before_scroll_page = int(0)

            while before_scroll_page != count_interests_in_page:
                before_scroll_page = count_interests_in_page
                interests_page_scroll = driver.find_element_by_xpath("//div[@class='entity-all pv-interests-list ml4 pt2 ember-view']//a")
                interests_page_scroll.send_keys(Keys.END)
                time.sleep(1.5)
                interests_page_content = driver.find_element_by_xpath("//div[@class='entity-list-wrapper ember-view']")
                count_interests_in_page = len(interests_page_content.find_elements_by_tag_name('li'))            
            
            for full_interest in interests_page_content.find_elements_by_tag_name('li'):  
                interest = full_interest.text.split('\n')[0]
                interests.append("name: "+interest)

    except NoSuchElementException:
        for user_interest in driver.find_elements_by_xpath("//li[@class='pv-interest-entity pv-profile-section__card-item ember-view']"):
            name_interest = user_interest.find_element_by_xpath(".//span[@class='pv-entity__summary-title-text']").text
            interests.append("name: "+ name_interest)

    return interests


def start_search(driver):
    with open('input.txt','r') as input:
        for n, user_id in enumerate(input, 1):
            user_id = user_id.rstrip('\n')
            driver.get('https://www.linkedin.com/in/'+user_id+'/')
            parsing_page(user_id,driver)

def print_result_to_file(driver):
    print(json.dumps(dictionary, indent=4, sort_keys=False, ensure_ascii=False))
    orig_stdout = sys.stdout
    f = open('output.txt', 'w',encoding='utf-8')
    sys.stdout = f

    print(json.dumps(dictionary, indent=4, sort_keys=False, ensure_ascii=False))

    sys.stdout = orig_stdout
    f.close()

driver = create_driver()
logins(driver)
start_search(driver)
print_result_to_file(driver)
