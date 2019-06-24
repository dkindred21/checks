import re
import sqlite3
from sqlite3 import Error

file = input('What file')
ck_database = 'check_req.db'

def create_connection(db_file):
	""" create a database connection to the check_req database
	:param db_file: database file
	:return: Connection object or none
	"""
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	
	return None
	
	
def create_table(conn, create_table_sql):
	
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
		
		
def written_parsed(file,ck_database):
	conn = create_connection(ck_database)
	try:
		c = conn.cursor()
	except Error as e:
		print(e)
	
	with open(file, 'r') as inFile:
		for _ in range(6):
			next(inFile)
		for line in inFile:
			if line[0].isdigit()  :
				line = line.strip()
				p_line = line[72:]
				p_line = re.sub(' +', ' ',p_line).split()
				new = int(p_line[0]),float(p_line[1])
				try:										
					c.execute('INSERT INTO written(check_no,amount)VALUES(?,?)',(new[0],new[1]))					
				except sqlite3.IntegrityError:
					pass
		conn.commit()
		
				
def view_db(ck_database):	
	conn = create_connection(ck_database)
	c = conn.cursor()
	for row in c.execute('SELECT * FROM written'):
		print(row)

def t_amount(ck_database):
	conn = create_connection(ck_database)
	c = conn.cursor()
	total = 'SELECT total(amount) FROM written'
	c.execute(total)
	return c.fetchone()[0]
	
def main():
	sql_create_written_table = """ CREATE TABLE IF NOT EXISTS written(
									 id INTEGER PRIMARY KEY,
									 check_no INTEGER TYPE UNIQUE,
									 amount FLOAT
									 );""" 
	
	sql_create_cashed_table = """ CREATE TABLE IF NOT EXISTS cashed(
									id INTEGER PRIMARY KEY,
									check_no INTEGER TYPE UNIQUE,
									amount FLOAT
									);"""
	
	conn = create_connection(ck_database)
	if conn is not None:
	# create written and cashed tables
		create_table(conn, sql_create_written_table)
		create_table(conn,sql_create_cashed_table)
	else:
		print("Error! cannot create the database connection.")

#this is a test
#this is a test2
	
if 	__name__ == '__main__':
	main()

