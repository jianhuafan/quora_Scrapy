from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_geo_info(user_url):
	# driver_location = '/Users/fanjianhua/Downloads/software for mac/phantomjs-2.1.1-macosx/bin/phantomjs'
	# driver = webdriver.PhantomJS(executable_path=driver_location)
	# try:
	# 	user_addr = driver.find_element_by_xpath("//span[@class='UserCredential IdentityCredential']").text
	# 	print(user_addr)
	# except NoSuchElementException:
	# 	print('no address!')
	# 	return

	html = urlopen(user_url)
	soup = BeautifulSoup(html, 'html.parser')
	user_info = soup.findAll('span', {'class': 'UserCredential IdentityCredential'})
	if user_info:
		for info in user_info:
			if info.get_text().startswith('Lives in'):
				user_addr = info.get_text()[9:]
				print(user_addr)
				return user_addr
	print('can not find infomation of address')
	return


if __name__ == '__main__':
	user_url = 'https://www.quora.com/profile/Andrew-Fedoniouk-1'
	get_geo_info(user_url)
