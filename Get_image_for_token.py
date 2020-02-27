# encoding: utf-8
import urllib.request as urllib
import sys
import datetime
import os
import requests, urllib
from selenium import webdriver
import time, shutil


class ScreenGet:
	urlGrafana = dict(
		defaultUrlStart='http://k10-fico-gm.vtb24.ru:3000/render/d-solo/000000021/ts-stats?orgId=1&panelId=',
		defaultUrlEnd2='&var-aggregation=5m&theme=light&width=1000&height=500&tz=Europe%2FMoscow')

	Grafana_logopas = {'grafana_user': 'Contractor_Technoserv',
					   'grafana_remember': '5023939560a415cb953f978af43a76858a1392c0dfc32a214601c1c7794148e61fe503f9357a68e91b53854ff2a69a8db7'}

	urlZabbix = dict(defaultUrlStart='http://k10-zabbix2-app/zabbix/chart2.php?graphid=',
					 period='&period=',
					 stime='&stime=',
					 isNow='&isNow=0&profileIdx=web.graphs&profileIdx2=',
					 width='&width=1782')

	pannelIdGrafana = dict(Request_count='2', Request_count_error='6', Prepare_time='10', Execute_time='11')

	pannelIdZabbix = dict(CPU_util_app1='7463', CPU_util_app2='7461', CPU_util_app3='7462',CPU_util_app4='15094',
						  Memory_all_app1='7370', Memory_all_app2='7365', Memory_all_app3='7366', Memory_all_app4='15105',
						  Memory_all_db='7369', GC_Statictics_app1='7437',
						  GC_Statictics_app2='7728', GC_Statictics_app3='7433', GC_Statictics_app4='15106',
						  Heap_Allocation_app1='7439', Heap_Allocation_app2='7730', Heap_Allocation_app3='7435',
						  Heap_Allocation_app4='15107',  Heap_Usage_app1='7427', Heap_Usage_app2='7425', Heap_Usage_app3='7426',
						  Heap_Usage_app4='15087',
						  JVM_Treads_app1='7447', JVM_Treads_app2='7445', JVM_Treads_app3='7446', JVM_Treads_app4='15089',
						  Thread_pool_Runtime_app1='7500', Thread_pool_Runtime_app2='7498',
						  Thread_pool_Runtime_app3='7499', Thread_pool_Runtime_app4='15102',
						  Flow_and_Fault_db='7573', HOLD_DB='7576',
						  JVM_Code_cashe_statictics_app1='8275', JVM_Code_cashe_statictics_app2='8273',
						  JVM_Code_cashe_statictics_app3='8274', JVM_Code_cashe_statictics_app4='15088',
						  K10TS2AUD_UNDOTBS='10814', K10TS2AUD_TEMP='10813',
						  K10TS2DB_UNDOTBS='9514', K10TS2DB_TEMP='9513', ActiveSessions_DB='9498')

	datB, datE, datBZabbix, datBZabbix, datBEZabbix, periodZabbix, pathSave = '', '', '', '', '', '', 'Screen'
	tokenName = 'TokenID'

	def __init__(self):
		print(sys.argv)
		self.datB = datetime.datetime.strptime(sys.argv[1], '%d.%m.%Y %H:%M')
		self.datE = datetime.datetime.strptime(sys.argv[2], '%d.%m.%Y %H:%M')
		self.datBEZabbix = str(self.datE)[0:4] + str(self.datE)[5:7] + str(self.datE)[8:10] + '_' + str(self.datB)[
																									11:13] + str(
			self.datB)[14:16] + '_' + str(self.datE)[11:13] + str(self.datE)[14:16]
		if len(sys.argv) > 3:
			self.pathSave = sys.argv[3]
		else:
			self.pathSave = os.curdir
		if os.path.exists(r'urls_success.txt') and os.path.exists(r'urls_fail.txt') == True:
			os.remove('urls_success.txt')
			os.remove('urls_fail.txt')

		if os.path.exists(self.pathSave + '\\Screen' + self.datBEZabbix):
			shutil.rmtree(self.pathSave + '\\Screen' + self.datBEZabbix)

		with open('urls_success.txt', 'w+') as url1:
			url1.write('')
		with open('urls_fail.txt', 'w+') as url1:
			url1.write('')
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix)
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix + '\\grafana')
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix + '\\zabbix')
		# if sys.argv[4] == 1:
		# 	self.get_passid()
		# else:
		# 	None

	def get_passid(self):
		os.environ['path'] += r';C:\Users\AstakhovAVl\Documents\ts2\chromedriver.exe'
		os.environ['PATH'] += r';C:\Users\AstakhovAVl\Documents\ts2\chromedriver.exe'
		print(os.environ['path'])
		print(os.environ['PATH'])
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument(
			'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3729.169 Safari/537.36')
		browser = webdriver.Chrome(sys._MEIPASS('./driver/chromedriver.exe'), options=options)

		# browser = webdriver.Chrome(options=options)
		browser.get('http://k10-fico-gm.vtb24.ru:3000/login')
		elemname = browser.find_elements_by_name('username')
		elemname[0].send_keys(str(self.Grafana_logopas.get('grafana_user')))  # log
		elemname = browser.find_elements_by_name('password')
		elemname[0].send_keys(str(self.password))  # pass)
		elemname = browser.find_elements_by_xpath('//*[@id="login-view"]/form/div[3]/button')
		elemname[0].click()
		time.sleep(3)
		self.Grafana_logopas.update({'grafana_remember': browser.get_cookies()[1].get('value')})
		print('request passid for grafana success', self.Grafana_logopas.get('grafana_remember'))

	def ConvertTime(self, timeIn, typeGraph=''):
		cTime = ''
		if typeGraph == 'grafana':
			cTime = str(timeIn.replace(tzinfo=datetime.timezone.utc).timestamp()).split('.')
			cTime = str(int(cTime[0] + cTime[1][:-2] + '000') - 10800000)
		if typeGraph == 'zabbix':
			self.datBZabbix = str(self.datB)[0:4] + str(self.datB)[5:7] + str(self.datB)[8:10] + str(self.datB)[
																								 11:13] + str(
				self.datB)[14:16]
			self.datEZabbix = str(self.datE)[0:4] + str(self.datE)[5:7] + str(self.datE)[8:10] + str(self.datE)[
																								 11:13] + str(
				self.datE)[14:16]
			self.periodZabbix = str((self.datE - self.datB).seconds)
		return cTime

	def Get_screen(self, pannelID='', pannelName='', typeGraph='', nameFileAdd=''):
		startTime, endTime = self.ConvertTime(self.datB, typeGraph), self.ConvertTime(self.datE, typeGraph)
		try:
			if typeGraph == 'grafana':
				url = self.urlGrafana.get(
					'defaultUrlStart') + pannelID + '&from=' + startTime + '&to=' + endTime + self.urlGrafana.get(
					'defaultUrlEnd2')
				# print(url)
				session = requests.Session()
				session.allow_redirects = False
				p = session.get(url, cookies=self.Grafana_logopas)
				# print(p)
				#print(session.cookies)
				with open(
						self.pathSave + '\\Screen' + self.datBEZabbix + '\\' + typeGraph + '\\' + nameFileAdd + '_' + pannelName + '.png',
						'wb') as out1:
					out1.write(p.content)
				with open(self.pathSave + '\\urls_success.txt', 'a') as url1:
					url1.write(url + '\n')
			if typeGraph == 'zabbix':
				url = self.urlZabbix.get('defaultUrlStart') + pannelID + self.urlZabbix.get(
					'period') + self.periodZabbix + self.urlZabbix.get('stime') + self.datBZabbix + self.urlZabbix.get(
					'isNow') + pannelID + self.urlZabbix.get('width')
				resource = urllib.request.urlopen(url)
				with open(
						self.pathSave + '\\Screen' + self.datBEZabbix + '\\' + typeGraph + '\\' + nameFileAdd + '_' + pannelName + '.png',
						'wb') as out1:
					out1.write(resource.read())
				with open(self.pathSave + '\\urls_success.txt', 'a') as url1:
					url1.write(url + '\n')
			print('' + pannelName + ' - screenshots created')
		except BaseException:
			print('error with panel: ' + pannelName)
			with open(self.pathSave + '\\urls_fail' + '.txt', 'a') as url1:
				url1.write(url + '\n')

	def updateToken(self):
		#print(self.Grafana_logopas)
		if os.path.exists(str(self.tokenName) + '.txt'):
			with open(self.tokenName + '.txt', 'r') as token:
				self.Grafana_logopas.clear()
				tokenId = str(token.readlines())[1:-1]
				print(str(tokenId)[1:-1])
			self.Grafana_logopas.update({'grafana_user': 'Contractor_Technoserv', 'grafana_remember': str(tokenId)[1:-1]})
		else:
			with open(self.tokenName + '.txt', 'w') as token:
				tokenId = self.Grafana_logopas.get('grafana_remember')
				print(tokenId)
				token.writelines(tokenId)
		print(self.Grafana_logopas)


	def CallSc(self):
		self.updateToken()
		j = 0
		for i in self.pannelIdGrafana:
			self.Get_screen(self.pannelIdGrafana[i], i, 'grafana')
		for i in self.pannelIdZabbix:
			j += 1
			self.Get_screen(self.pannelIdZabbix[i], i, 'zabbix', str(j))


if __name__ == '__main__':
	SC = ScreenGet()
	SC.CallSc()
	print('Program execute')
