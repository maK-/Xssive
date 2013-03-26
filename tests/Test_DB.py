import web, string
from time import time

#Comment out the following line for debug messages.
web.config.debug = False

"""
Database class allows easier control of the data
"""
class Database:
	#On initializing replace default values
	def __init__(self, db_type, db_data):
		self.db_type = db_type
		self.db_data = db_data
		self.data = None
		self.db = None
	
	#This creates a database of either type and creates a table to use
	def Create_DB(self):
		#For Mysql
		if self.db_type == 'mysql' and self.db_data != None:
			try:
				self.data = string.split(self.db_data, ',')
				self.db = web.database(dbn=self.db_type, host=self.data[0], user=self.data[1], pw=self.data[2], db=self.data[3])
				self.db.query('CREATE TABLE IF NOT EXISTS xssive_test (victimid INT(10) NOT NULL, ip VARCHAR(20) NOT NULL, browser VARCHAR(200) NOT NULL, datetime INT(20) NOT NULL, victimdata VARCHAR(5000) NOT NULL);')
			except:
				print '\033[31mError: Problem creating MySQL Database or Table Already Exists.\033[0m'
		
		#For Sqlite
		if self.db_type == 'sqlite' and self.db_data != None:
			try:
				self.db = web.database(dbn=self.db_type, db=self.db_data)
				self.db.query('CREATE TABLE IF NOT EXISTS xssive_test (victimid INT, ip STRING, browser STRING, datetime INT, victimdata STRING);')
			except:
				print '\033[31mError: Local Database could Not be created or Table already Exists.\033[0m'
	
	
	#This function is used to test our Database.
	def Stat_DB(self):
		if self.db_type == 'sqlite':
			db_size = self.db.query('SELECT COUNT(*) as size from xssive_test')
			cols = self.db.query('Pragma table_info(xssive_test);')
			col_num = 0	
			col_names = '|'

			for i in cols:
				col_num += 1
				col_names += str(i['name'])+'|'

			print '\033[37mMYSQL:Number of Database entries: '+str(db_size[0].size)
			print 'MYSQL:Number of Columns in table: '+str(col_num)
			print 'MYSQL:Column Names = '+col_names+'\033[31m'
		
		
		if self.db_type == 'mysql':
			db_size = self.db.query('SELECT COUNT(*) as size from xssive_test')

			cols = self.db.query('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA="'+self.data[3]+'" AND TABLE_NAME="xssive_test";')
			col_num = 0
			col_names = '|'
			
			for i in cols:
				col_num +=1
				col_names += str(i['COLUMN_NAME'])+'|'
			print '\033[37mSQLITE:Number of Database entries: '+str(db_size[0].size)
			print 'SQLITE:Number of Columns in table: '+str(col_num)
			print 'SQLITE:Column Names = '+col_names+'\033[0m'


	def Test_Func(self, count):
		print '\033[4m\033[037mTESTING DATABASE FUNCTIONALITY\033[0m'
		#Testing Insert function
		for i in range(0, count):
			self.db.insert('xssive_test', victimid=666,ip="127.0.0.1",browser='Firefox', datetime=int(time()),victimdata='<iframe> TEST </iframe>')
		#Testing Select function
		select = self.db.select('xssive_test')
		for i in select:
			print 'Select: '+str(i['victimid'])+','+i['ip']+','+i['browser']+','+str(i['datetime'])+','+i['victimdata']

	def Drop_Test(self):
		self.db.query('DROP TABLE xssive_test;')

if __name__=="__main__":
	"""
	This test is to ensure database functionality.
	"""
	#This will create a sqlite database called test.db
	db = Database('sqlite', 'test.db')
	db.Create_DB()
	db.Test_Func(5)
	db.Stat_DB()
	db.Drop_Test()	

	#With this test you must provide your mysql information
	#Please use the following order. "host,username,password,dbname"
	db_mysql = Database('mysql', 'localhost,mak,p00pH4x,test')
	db_mysql.Create_DB()
	db_mysql.Test_Func(5)
	db_mysql.Stat_DB()
	db_mysql.Drop_Test()	
