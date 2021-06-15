from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys 
import re
import pandas as pd

driver = webdriver.Firefox()
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')

# Replace the ... by username 
username.send_keys('...')

password = driver.find_element_by_id('session_password')

# Replace the ... by password 
password.send_keys('...')

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

log_in_button.click()
# Replace the ... by Jobs url 

driver.get('...')
html = driver.page_source
soup = BeautifulSoup(html,'lxml')
Applicants=[]

Class = soup.findAll('li', {'class': 'hiring-applicants__list-item'})
for Sub in Class:
    Applicants.append('https://www.linkedin.com'+str(Sub.find("a").get('href')))

applicant_details=[]
final_values_of_applicant=[['Name','Email ID','Phone No','Profile Link']]

for i in Applicants:
    driver.get(i)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    Profile = soup.findAll('div', {'class': 'hiring-profile-highlights__see-full-profile'})
    for Sub in Profile:
        Profile_Url = 'https://www.linkedin.com'+str(Sub.find("a").get('href'))
        applicant_details.append(Profile_Url)
    
    try:
        print(driver.find_elements_by_xpath("//*[@class='artdeco-button artdeco-button--secondary artdeco-button--muted artdeco-button--3 artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view']")[0].click())
    except:
        pass

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    print(applicant_details)
    Profile = soup.findAll('div', {'class': 'display-flex flex-column align-items-flex-start'})
    j=''

    for applicant_details_in_more in Profile:
        temp_list=[]
        Profile_name= soup.findAll('h1', {'class': 'display-flex align-items-center t-24'})
        s,e=str(Profile_name).index('>'),str(Profile_name).index("application")
        temp_list.append(str(Profile_name)[s+len('\n')+len('\n')+8:e-3])
        got_text=applicant_details_in_more.find("span").text
        Current_values = [x for x in got_text.split(' ') if x]

        if re.search( '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$' , str( Current_values[-1] ) ):
            j=Current_values[-1]

        elif re.findall( '[+]91\d{10}',str( Current_values[-3] ) ) or re.search( '\d{10}',str ( Current_values[-3] ) ):
            temp_list.append(j.rstrip("\n"))
            temp_list.append(Current_values[-3])

        temp_list.append(Profile_Url)

        if len(temp_list)>2:
            final_values_of_applicant.append(temp_list)

        print(final_values_of_applicant)
        
df=pd.DataFrame(final_values_of_applicant)
df.to_csv('data.csv',index=False,header=False)
print(final_values_of_applicant)
