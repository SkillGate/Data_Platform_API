from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup

def extract_linkedIn_skills_and_recommendation_data(linkedInUrl):
    result = []
    result = {
        'skills_list': extract_linkedIn_skills(linkedInUrl),
        'recommendation_list': extract_linkedIn_recommendations(linkedInUrl)
    }

    return result


def extract_linkedIn_skills(linkedInUrl):
    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')

    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys('ashaniimalsha126@gmail.com')

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys('Imalsha@26')

    button = driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button')
    button.click()

    profile_url = linkedInUrl
    skill_url = profile_url + '/details/skills/'


    driver.get(skill_url)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    skills_list = []

    skill_section_div = soup.find('div', class_='scaffold-finite-scroll__content')

    skill_elements = skill_section_div.find_all('li', class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')

    if skill_elements:

        for div in skill_elements:
            
            skill_dict = {}

            skill_name_div = div.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
            if skill_name_div:
                skill_dict['skill_name'] = skill_name_div.find('span', class_='').text.strip()
                

            endorsed_div = div.find('div', class_='hoverable-link-text display-flex align-items-center t-14 t-normal t-black')
            if endorsed_div:
                skill_dict['endorsed'] = endorsed_div.find('span', class_='').text.strip()
                

            utilize_div = div.find('div', class_='PEEijEvVHiwJqBBeMYIsBNXeVOxmrXcLGE inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width')
            if utilize_div:
                skill_dict['utilize'] = utilize_div.find('span', class_='').text.strip()

            skills_list.append(skill_dict)

    return skills_list



def extract_linkedIn_recommendations(linkedInUrl):

    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/login')

    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys('ashaniimalsha126@gmail.com')

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys('Imalsha@26')

    button = driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button')
    button.click()

    profile_url = linkedInUrl
    recommendation_url = profile_url

    driver.get(recommendation_url)

    rec_html_content = driver.page_source

    soup = BeautifulSoup(rec_html_content, "html.parser") 

    recommendations_list = []

    section_elements = soup.find_all('section')
    print(section_elements)
    for section in section_elements:
        
        recommendations_div = section.find('div', id='recommendations')
        if recommendations_div:
        
            recieved_rec_section = section.find('div', class_='artdeco-tabpanel active ember-view')
            rec_elements = recieved_rec_section.find_all('div', class_='display-flex flex-column full-width align-self-center')
            for rec in rec_elements:
                print(rec)
                rec_dict = {}

                name_div = rec.find('div', class_='display-flex align-items-center mr1 hoverable-link-text t-bold')
                if name_div:
                    rec_dict['name'] = name_div.find('span').text.strip()

                description_div = rec.find('div', class_='sQMsmklQenCdtUbauBOumjhpeyIVajOkOeo inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width')
                if description_div:
                    rec_dict['description'] = description_div.find('span').text.strip()

                recommendations_list.append(rec_dict)

            break


    return recommendations_list





                
            
