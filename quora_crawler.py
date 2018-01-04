from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from time import sleep
# from login import add_cookies, login
import argparse
import os
from question import *
from user import *

def get_user_addr(content, topic):
	curr_line = 0
	user_addr_list = []
	while curr_line < len(content):
		user_url = content[curr_line]
		print(user_url)
		if len(user_url) >1:
			user_addr = get_geo_info(user_url)
			if user_addr is not None:
				user_addr_list.append(user_addr)
		curr_line += 1

	user_addr_list_path = 'data/user/{}_user_addr'.format(topic)
	with open(user_addr_list_path, 'a') as f:
		for addr in user_addr_list:
			f.write('%s\n' % addr)
	f.close()

def get_answer(content, answer_limit, driver_location, topic):
	curr_line = 0
	while curr_line < len(content):
		q_url = content[curr_line]
		get_info(q_url, answer_limit, driver_location, topic)
		curr_line += 1

def get_topic_url(topic):
	return 'https://www.quora.com/topic/' + topic + '/all_questions'

def get_question_url(topic, question_limit, driver_location):
	topic_url = get_topic_url(topic)
	html = urlopen(topic_url)
	soup = BeautifulSoup(html, 'html.parser')
	mydivs = soup.findAll('a', {'class': 'question_link'})

	driver = webdriver.PhantomJS(executable_path=driver_location)
	# add_cookies(driver)
	driver.get(topic_url)

	while True:
		print('scrollTo')
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		sleep(5)

		user_elems = driver.find_elements_by_xpath("//a[@class='question_link']")
		cnt = len(user_elems)
		print('current number of question: %s\n' % cnt)
		if cnt == 0:
			return
		if cnt >= question_limit:
			break

	question_count = 0
	question_list_path = 'data/topic/{}_question_list'.format(topic)
	try:
		os.remove(question_list_path)
	except OSError:
		pass
	with open(question_list_path, 'a') as f:
		for elem in user_elems:
			if question_count >= question_limit:
				f.close()
				break
			f.write('%s\n' % elem.get_attribute('href'))
			question_count += 1
	f.close()

	driver.close()




def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--topic', type=str, default='Python-programming-language-1', help='topic name')
	parser.add_argument('--question_limit', type=int, default=100, help='maximum number of questions for a given topic')
	parser.add_argument('--answer_limit', type=int, default=30, help='maximum number of answers for a given question')
	parser.add_argument('--driver_location', type=str, default='/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs', help='location of chromedriver')
	args = parser.parse_args()
	get_question_url(args.topic, args.question_limit, args.driver_location)

	question_list_path = 'data/topic/{}_question_list'.format(args.topic)
	try:
		with open(question_list_path) as f:
			content = f.readlines()
	except IOError as e:
		print('I/O error: {}'.format(e))
	except:
		print('Unexpected error')
		raise
	get_answer(content, args.answer_limit, args.driver_location, args.topic)

	user_url_list_path = 'data/user/{}_user_url_list'.format(args.topic)
	try:
		with open(user_url_list_path) as f:
			content = f.readlines()
	except IOError as e:
		print('I/O error: {}'.format(e))
	except:
		print('Unexpected error')
		raise
	get_user_addr(content, args.topic)

	
if __name__ == '__main__':
	main()