import pymysql

def dump_question_into_db(q_info, table):
	conn = pymysql.connect(host='localhost', user='root', password='119911', db='quora_db', charset='utf8')
	cursor = conn.cursor()

	cursor.execute('USE quora_db')

	sql = 'INSERT INTO ' + table + '(question_title, q_url, answer_cnt, question_details) VALUES (%s, %s, %s, %s)'
	
	try:
		cursor.execute(sql, q_info)
		conn.commit()
	except Exception as e:
		print('error occured when inserting into question:{}'.format(e))
		conn.rollback()
		conn.close()
		return False
	cursor.close()
	conn.close()
	return True

def dump_answer_into_db(ans_info, table):
	conn = pymysql.connect(host='localhost', user='root', password='119911', db='quora_db', charset='utf8')
	cursor = conn.cursor()

	cursor.execute('USE quora_db')

	sql = 'INSERT INTO ' + table + ' (question_title, user_name, user_url, views, upvotes) values (%s, %s, %s, %s, %s)'
	try:
		cursor.executemany(sql, ans_info)
		conn.commit()
	except Exception as e:
		print('error occured when inserting into answer:{}'.format(e))
		conn.rollback()
		conn.close()
		return False
	cursor.close()
	conn.close()
	return True

if __name__ == '__main__':

	conn = pymysql.connect(host='localhost', user='root', password='119911', db='quora_db', charset='utf8')
	cursor = conn.cursor()

	cursor.execute('USE quora_db')

	# cursor.execute('create table question (question_title varchar(1000) not null, q_url varchar(1000), answer_cnt int, question_details varchar(10000), primary key (question_title));')
	# cursor.execute('create table answer (question_title varchar(1000), user_name varchar(1000), user_url varchar(1000), views int, upvotes int, primary key (question_title, user_name));')

	sql = 'select * from question'

	# sql = 'select * from answer'
	sql = 'truncate table question'

	cursor.execute(sql)

	cursor.close()
	conn.close()

	temple_q = ('cc', 'aa', 3, 'bb')
	temple_a = ('hh', 'aa', 'cc', 3, 4)
	# temple_q = ('dd', 'jj')

	# dump_question_into_db(temple_q, 'question')
	# dump_answer_into_db(temple_a, 'answer')




