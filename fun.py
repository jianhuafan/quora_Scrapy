from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.PhantomJS(executable_path='/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs')
q_url = 'https://www.quora.com/What-is-the-most-shocking-substitution-in-a-football-match'
driver.get(q_url)
time.sleep(5)
source = requests.get(q_url)

soup = BeautifulSoup(source.text, 'html.parser')

upvote_elem = soup.find("div", {"class": "ExpandedQTextExpandedAnswer"}).get_text()
print(upvote_elem)

# xpath = "//a[@action_click='AnswerUpvote']//span[@class='count']"
xpath = "//span[contains(@class, 'count')]"
# xpath = ".//span[@class='meta_num']"
try:
	ans_vote = driver.find_element_by_xpath(".//a[@class='AnswerVoterListModalLink VoterListModalLink']").text
	print(ans_vote)
except NoSuchElementException:
	print('shit!')



