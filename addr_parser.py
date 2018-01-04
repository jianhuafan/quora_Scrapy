import re

def get_addr_data(content):
	curr_line = 0
	addr_dict = {}
	while curr_line < len(content):
		user_addr = content[curr_line].strip('\n')
		temp = re.split(',', user_addr)
		if temp[0].startswith('I Live in'):
			real_addr = temp[0][9:]
		else:
			real_addr = temp[0]
		if real_addr not in addr_dict:
			addr_dict[real_addr] = 1
		else:
			addr_dict[real_addr] += 1
		curr_line += 1
	return geoChartTable(addr_dict)

def geoChartTable(addr_dict):

	geoTable = []
	geoTable.append(['Region', 'Number'])
	for region, count in addr_dict.items():
		geoTable.append([region, count])
	return geoTable

def main():
	user_addr_path = 'data/user/Python-programming-language-1_user_addr'
	try:
		with open(user_addr_path) as f:
			content = f.readlines()
	except IOError as e:
		print('I/O error: {}'.format(e))
	except:
		print('Unexpected error')
		raise

	geoTable = get_addr_data(content)
	print(geoTable)

if __name__ == '__main__':
	main()
