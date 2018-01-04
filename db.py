import pymysql

def dump_question_into_db(q_info, table):
	conn = pymysql.connect(host='localhost', user='root', password='119911', db='quora_db', charset='utf8')
	cursor = conn.cursor()

	cursor.execute('USE quora_db')

	sql = 'INSERT INTO ' + table + '(question_title, q_url, answer_cnt) VALUES (%s, %s, %s)'
	
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

	sql = 'INSERT INTO ' + table + ' (question_title, user_name, user_url, views) values (%s, %s, %s, %s)'
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

	cursor.execute('create table if not exists question (question_id int not null auto_increment, question_title varchar(255) not null, q_url varchar(255), answer_cnt int, primary key (question_id));')
	cursor.execute('create table if not exists answer (answer_id int not null auto_increment, question_title varchar(255), user_name varchar(255), user_url varchar(255), views int, primary key (answer_id));')

	# sql = 'select * from question'

	# sql = 'select * from answer'
	# sql = 'truncate table question'

	# cursor.execute(sql)

	cursor.close()
	conn.close()

	# temple_q = ('cc', 'aa', 3, 'bb')
	# temple_a = ('hh', 'aa', 'cc', 3, 4)
	# temple_q = ('dd', 'jj')

	# dump_question_into_db(temple_q, 'question')
	# dump_answer_into_db(temple_a, 'answer')




