from selenium import webdriver
import pickle as cPickle

def login():
	user = ''
	password = ''

	driver = webdriver.PhantomJS(executable_path='/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs')
	driver.get('https://www.quora.com/')
	driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys(user)
	driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
	while driver.find_element_by_xpath("//input[@value='Login']") != []:
		driver.find_element_by_xpath("//input[@value='Login']").click()

	cPickle.dump(driver.get_cookies(), open('data/cookies.pkl', 'w'))


def add_cookies(driver):
	cookies = cPickle.load(open('data/cookies.pkl'))
	for cookie in cookies:
		driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path')})


