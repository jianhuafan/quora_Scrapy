from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
import re
from time import sleep
from login import add_cookies, login

def get_question_url(topic_url):
	html = urlopen(topic_url)
	soup = BeautifulSoup(html)
	mydivs = soup.findAll('a', {'class': 'question_link'})

	driver = webdriver.PhantomJS(executable_path='/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs')
	# add_cookies(driver)
	driver.get(topic_url)

	while True:
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		sleep(5)

		user_elems = driver.find_elements_by_xpath("//a[@class='question_link']")
		cnt = len(user_elems)
		if cnt == 0:
			return

	with open('data/question_url_list', 'a') as f:
		for elem in user_elems:
			f.write('%s\n' % elem.get_attribute('href'))

	driver.close()


def main():
	topic_url = 'https://www.quora.com/topic/Python-programming-language-1/all_questions'
	get_question_url(topic_url)
	



if __name__ == '__main__':
	main()