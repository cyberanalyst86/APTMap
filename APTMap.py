from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import datetime
import re

#------------------------------Declare Variables------------------------------#

Industry_class_list = []
APT_list = []
Location_list = []
Description_list = []
Other_names_list = []
Associated_groups_list = []
First_seen_list = []
Sponsor_list = []
Motivation_list = []
Targets_list = []
Tools_list = []
Show_details_list = []

#------------------------------Sector to Query------------------------------#
#sector_to_query = "aviation"
sector_to_query = "aerospace"

#------------------------------Get Date of Query------------------------------#

now = datetime.datetime.now()
date_stamp = now.strftime("%d_%m_%Y")

#------------------------------Define Output File Path for Excel------------------------------#

output_filepath = "C:\\Users\\Admin\\Downloads\\aptmap\\"+ str(date_stamp)+ "_" + str(sector_to_query) + ".xlsx"

#----------------------------APTMap Query URL------------------------------#

login_url = "https://andreacristaldi.github.io/APTmap/"

#----------------------------Initialize the Chrome Driver------------------------------#

driver = webdriver.Chrome(r"chromedriver")

#------------------------------Get into APT MAP------------------------------#

driver.get(login_url)
driver.maximize_window()
driver.implicitly_wait(0.2)

#------------------------------Click on Go To Map------------------------------#

driver.find_element("id", "start-globe").click()
driver.implicitly_wait(0.2)
#------------------------------Click on Search------------------------------#
xpath = "//*[@id=\"search\"]/h3"
driver.find_elements("xpath", xpath)[0].click()
driver.implicitly_wait(0.2)
#------------------------------Click on Search (by filter)------------------------------#
driver.find_element("id", "searchTarget").send_keys(sector_to_query)
driver.implicitly_wait(0.2)
driver.find_element("id", "btnsearch").click()


#------------------------------Scrap Data------------------------------#
#aviation 1 - 13
#aerospace 1 - 22
for i in range(1, 13):

    xpath = "//*[@id=\"searchPlaceHolder\"]/li[" + str(i) + "]"
    info = driver.find_elements("xpath", xpath)[0].text

    APT_list.append(list(info.split("\n"))[0])

    Location_list.append(re.findall(r"Location:.*", info))

    Description_list.append(re.findall(r"Description:.*", info))

    Other_names_list.append(re.findall(r"Other names.*", info))

    Associated_groups_list.append(re.findall(r"Associated groups:.*", info))

    First_seen_list.append(re.findall(r"First seen:.*", info))

    Sponsor_list.append(re.findall(r"Sponsor:.*", info))

    Motivation_list.append(re.findall(r"Motivation:.*", info))

    Targets_list.append(re.findall(r"Targets:.*", info))

    Tools_list.append(re.findall(r"Tools:.*", info))

for i in range(len(APT_list)):
    Industry_class_list.append("Aviation")

#------------------------------Create Dataframe------------------------------#

data = {'APT' : APT_list,
                      'Location' : Location_list,
                      'Description' : Description_list,
                      'Other names': Other_names_list,
                      'Associated groups': Associated_groups_list,
                      'First seen': First_seen_list,
                      'Sponsor': Sponsor_list,
                      'Motivation': Motivation_list,
                      'Targets': Targets_list,
                      'Tools': Tools_list,
                      'Industry Class': Industry_class_list
                      }

df = pd.DataFrame(data)

#------------------------------Output Dataframe to Excel------------------------------#

df.to_excel(output_filepath, index=False)

# close the driver
driver.close()