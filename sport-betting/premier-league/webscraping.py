# https://www.youtube.com/watch?v=kmvZvJbR50E&list=PLsvYG12RCRU42ST9mHyuAcPYYJNcwYGeY&index=12

import pandas as pd
import numpy as np
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, "/usr/lib/chromium-browser/chromedriver")

# Instancing the object ChromeOptions and defining some options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Creating the Chorme's WebDriver 
wb_driver_chrome = webdriver.Chrome("chromedriver", options=options)

match = {'Date':[],'Time':[],'Country':[],'League':[],'Home':[],'Away':[],'Odds_H':[],'Odds_D':[],'Odds_A':[]}

# Accessing the site with the WebDriver
wb_driver_chrome.get("https://www.flashscore.com/")
id_matches = []
matches = wb_driver_chrome.find_elements(By.CSS_SELECTOR, "div.event__match--scheduled")

# Append match's ID in list
for match in matches:
    id_matches.append(match.get_attribute("id"))

id_matches = [match[4:] for match in id_matches]
for link in id_matches:
    wb_driver_chrome.get(f'https://www.flashscore.com/match/{link}/#/match-summary')
    try:
        date = wb_driver_chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__startTime').text.split(' ')[0]
        time = wb_driver_chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__startTime').text.split(' ')[1]
        country = wb_driver_chrome.find_element(By.CSS_SELECTOR,'span.tournamentHeader__country').text.split(':')[0]
        league = wb_driver_chrome.find_element(By.CSS_SELECTOR,'span.tournamentHeader__country')
        league = league.find_element(By.CSS_SELECTOR,'a').text
        home = wb_driver_chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__home')
        home = home.find_element(By.CSS_SELECTOR,'div.participant__participantName').text
        away = wb_driver_chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__away')
        away = away.find_element(By.CSS_SELECTOR,'div.participant__participantName').text
    except:
          pass
    print(date, time, country, league, home, away) 