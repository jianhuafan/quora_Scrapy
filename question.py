from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from db import dump_question_into_db, dump_answer_into_db


def get_upvotes(cnt):
	if cnt[-1].isdigit():
		cnt = int(cnt)
	elif cnt[-1] == 'k':
		cnt = int(float(cnt[:-1]) * 1000)
	elif cnt[-1] == 'm':
		cnt = int(float(cnt[:-1]) * 1000000)
	return cnt

def get_views(follower):
	follower = follower.strip().split()[0]
	print(follower)
	mul = 1
	factors = follower.split(',')
	res = 0
	for factor in factors[::-1]:
		res += (int(factor)*mul)
		mul *= 1000
	return res



def get_info(q_url):
	driver = webdriver.PhantomJS(executable_path='/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs')
	from login import add_cookies
	# add_cookies(driver)

	driver.get(q_url)
	try:
		cnt_answers = driver.find_element_by_xpath("//div[@class='answer_count']").text.strip().split()[0]
		if cnt_answers[-1].isdigit():
			cnt_answers = int(cnt_answers)
		else:
			cnt_answers = int(cnt_answers[:-1])
	except NoSuchElementException:
		print('no answer yet!')
		return
	
	question_title = driver.find_element_by_xpath("//div[@class='header']//span[@class='rendered_qtext']").text.strip()
	print('question: {}'.format(question_title))
	try:
		question_details = driver.find_element_by_xpath("//div[@class='question_details']").text
		print('question details:{}'.format(question_details))
	except NoSuchElementException:
		print('no details for the question')
		question_details = 'no details'

	print('answer numbers:{}'.format(cnt_answers))

	try:
		stats_elem = driver.find_element_by_xpath("//div[@class='QuestionStats']")
		followers = get_views(stats_elem.find_element_by_xpath("./span[1]").text)
		print('numbers of followers: {}'.format(followers))
		views = get_views(stats_elem.find_element_by_xpath("./span[2]").text)
		print('numbers of views: {}'.format(views))
		asked_date = get_question_date(stats_elem.find_element_by_xpath("./span[3]").text)
		print('dates of question: {}'.format(asked_date))
		tag_elems = driver.find_element_by_xpath("//span[contains(@class, 'TopicNameSpan')]")
		tags = ''
		if len(tag_elems):
			tags = ','.join([elem.text for elem in tag_elems])
			print('question tags: {}'.format(tags))
	except NoSuchElementException:
		print('no statistics for this question')

	ans_info = []
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(3)

		user_elems = driver.find_elements_by_xpath(
            "//div[@class='pagedlist_item']//a[starts-with(@name,'answer_')]/following-sibling::div[@class='Answer AnswerBase']")
		cnt = len(user_elems)
		print(question_title, cnt)
		if cnt >= cnt_answers:
			break
		
	true_ans_num = 0
	for idx, elem in enumerate(user_elems):
		try:
			link_elem = elem.find_element_by_xpath(".//a[starts-with(@class,'user')]")
			user_name = link_elem.text.strip()
			user_url = link_elem.get_attribute('href').strip()
			print('name:{}, link:{}'.format(user_name, user_url))
		except NoSuchElementException:
			user_name = elem.find_element_by_xpath(".//span[contains(@class,'anon_user')]").text
			user_url = ''
			print('name:{}'.format(user_name))

		text = elem.find_element_by_xpath(".//span[@class='ui_qtext_rendered_qtext']").text
		# print('text:{}'.format(' '.join(map(lambda x: x.strip(), text.split()))))
		# answer_date = get_answer_date(elem.find_element_by_xpath(".//a[@class='answer_permalink']").text)
		# print('answer date:{}'.format(answer_date))

		try:
			ans_views = get_upvotes(elem.find_element_by_xpath(".//span[@class='meta_num']").text)
			print('num of views:{}'.format(ans_views))
		except NoSuchElementException:
			ans_views = 0
			print('num of views:{}'.format(ans_views))

		try:
			ans_vote = get_upvotes(elem.find_element_by_xpath(".//a[@action_click='AnswerUpvote']//span[@class='count']").
                    text)
			print('upvotes:{}'.format(ans_vote))
		except NoSuchElementException:
			ans_vote = 0
			print('upvotes:{}'.format(ans_vote))
		ans_info.append((question_title, user_name, user_url, ans_views, ans_vote))
		true_ans_num += 1

	if dump_question_into_db((question_title, q_url, true_ans_num, question_details), 'question'):
		dump_answer_into_db(ans_info, 'answer')

	driver.close()








if __name__ == '__main__':
	q_url = 'https://www.quora.com/If-I-write-a-Python-program-then-will-it-run-faster-than-Java-If-no-then-how-can-it-run-faster-than-Java'
	get_info(q_url)