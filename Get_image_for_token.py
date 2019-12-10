import urllib.request as urllib
import sys
import datetime
import os
import requests, urllib


class ScreenGet:
	urlGrafana = dict(
		defaultUrlStart='http://k10-fico-gm.vtb24.ru:3000/render/d-solo/000000021/ts-stats?orgId=1&panelId=',
		defaultUrlEnd2='&var-aggregation=5m&theme=light&width=1000&height=500&tz=Europe%2FMoscow')

	Grafana_logopas = dict(grafana_user='Contractor_Technoserv',
						   grafana_remember='5023939560a415cb953f978af43a76858a1392c0dfc32a214601c1c7794148e61fe503f9357a68e91b53854ff2a69a8db7')

	urlZabbix = dict(defaultUrlStart='http://k10-zabbix2-app/zabbix/chart2.php?graphid=',
					 period='&period=',
					 stime='&stime=',
					 isNow='&isNow=0&profileIdx=web.graphs&profileIdx2=',
					 width='&width=1782')

	pannelIdGrafana = dict(Request_count='2', Request_count_error='6', Prepare_time='10', Execute_time='11')

	pannelIdZabbix = dict(CPU_util_app1='7463', CPU_util_app2='7461', CPU_util_app3='7462', Memory_all_app1='7370',
						  Memory_all_app2='7365', Memory_all_app3='7366', Memory_all_db='7369',
						  GC_Statictics_app1='7437', GC_Statictics_app2='7728', GC_Statictics_app3='7433',
						  Heap_Allocation_app1='7439', Heap_Allocation_app2='7730', Heap_Allocation_app3='7435',
						  Heap_Usage_app1='7427', Heap_Usage_app2='7425', Heap_Usage_app3='7426',
						  JVM_Treads_app1='7447', JVM_Treads_app2='7445', JVM_Treads_app3='7446',
						  Thread_pool_Runtime_app1='7500', Thread_pool_Runtime_app2='7498',
						  Thread_pool_Runtime_app3='7499',
						  Flow_and_Fault_db='7573', HOLD_DB='7576',
						  JVM_Code_cashe_statictics_app1='8275', JVM_Code_cashe_statictics_app2='8273',
						  JVM_Code_cashe_statictics_app3='8274',
						  K10TS2AUD_UNDOTBS='10814', K10TS2AUD_TEMP='10813',
						  K10TS2DB_UNDOTBS='9514', K10TS2DB_TEMP='9513')

	datB, datE, datBZabbix, datBZabbix, datBEZabbix, periodZabbix, pathSave = '', '', '', '', '', '', 'Screen'

	def __init__(self):
		self.datB = datetime.datetime.strptime(sys.argv[1], '%d.%m.%Y %H:%M')
		self.datE = datetime.datetime.strptime(sys.argv[2], '%d.%m.%Y %H:%M')
		self.datBEZabbix = str(self.datE)[0:4] + str(self.datE)[5:7] + str(self.datE)[8:10] + '_' + str(self.datB)[
																									11:13] + str(
			self.datB)[14:16] + '_' + str(self.datE)[11:13] + str(self.datE)[14:16]
		self.pathSave = sys.argv[3]
		if os.path.exists(r'urls_success.txt') and os.path.exists(r'urls_fail.txt') == True:
			os.remove('urls_success.txt')
			os.remove('urls_fail.txt')
		with open('urls_success.txt', 'w+') as url1:
			url1.write('')
		with open('urls_fail.txt', 'w+') as url1:
			url1.write('')
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix)
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix + '\\grafana')
		os.mkdir(self.pathSave + '\\Screen' + self.datBEZabbix + '\\zabbix')

	def ConvertTime(self, timeIn, typeGraph=''):
		cTime = ''
		if typeGraph == 'grafana':
			cTime = str(timeIn.replace(tzinfo=datetime.timezone.utc).timestamp()).split('.')
			cTime = str(int(cTime[0] + cTime[1][:-2] + '000')-10800000)
		if typeGraph == 'zabbix':
			self.datBZabbix = str(self.datB)[0:4] + str(self.datB)[5:7] + str(self.datB)[8:10] + str(self.datB)[
																								 11:13] + str(
				self.datB)[14:16]
			self.datEZabbix = str(self.datE)[0:4] + str(self.datE)[5:7] + str(self.datE)[8:10] + str(self.datE)[
																								 11:13] + str(
				self.datE)[14:16]
			self.periodZabbix = str((self.datE - self.datB).seconds)
		return cTime

	def Get_screen(self, pannelID='', pannelName='', typeGraph=''):
		startTime, endTime = self.ConvertTime(self.datB, typeGraph), self.ConvertTime(self.datE, typeGraph)
		try:
			if typeGraph == 'grafana':
				url = self.urlGrafana.get(
					'defaultUrlStart') + pannelID + '&from=' + startTime + '&to=' + endTime + self.urlGrafana.get(
					'defaultUrlEnd2')
				session = requests.Session()
				session.allow_redirects = False
				p = session.get(url, cookies=self.Grafana_logopas)
				with open(self.pathSave + '\\Screen' + self.datBEZabbix + '\\' + typeGraph + '\\' + pannelName + '_' + self.datBEZabbix + '.png', 'wb') as out1:
					out1.write(p.content)
				with open(self.pathSave + '\\urls_success.txt', 'a') as url1:
					url1.write(self.pathSave + url + '\n')
			if typeGraph == 'zabbix':
				url = self.urlZabbix.get('defaultUrlStart') + pannelID + self.urlZabbix.get(
					'period') + self.periodZabbix + self.urlZabbix.get('stime') + self.datBZabbix + self.urlZabbix.get(
					'isNow') + pannelID + self.urlZabbix.get('width')
				resource = urllib.request.urlopen(url)
				with open(self.pathSave + '\\Screen' + self.datBEZabbix + '\\' + typeGraph + '\\' + pannelName + '.png', 'wb') as out1:
					out1.write(resource.read())
				with open(self.pathSave + '\\urls_success.txt', 'a') as url1:
					url1.write(url + '\n')
			print('' + pannelName + ' - screenshots created')
		except BaseException:
			print('error with panel: ' + pannelName)
			with open(self.pathSave + '\\urls_fail' + '.txt', 'a') as url1:
				url1.write(self.pathSave + url + '\n')


	def CallSc(self):
		for i in self.pannelIdGrafana:
			self.Get_screen(self.pannelIdGrafana[i], i, 'grafana')
		for i in self.pannelIdZabbix:
			self.Get_screen(self.pannelIdZabbix[i], i, 'zabbix')


if __name__ == '__main__':
	SC = ScreenGet()
	SC.CallSc()
	print('Program execute')
