import re
import paramiko
from datetime import datetime, date, time, timedelta
import time
import threading
import os
import linecache
import sys



class SshClient:
	strings = ''
	local_dir = sys.argv[0][:-10]

	def __init__(self):
		self.copy_file()
		with open(str(self.local_dir + 'jmsCountLog.txt'), 'r+', encoding='utf-8') as file1:
			self.strings = file1.readlines()
		self.print_jms()

	def copy_file(self):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname='k10-ts2-app01.vtb24.ru', username='weblogic', password='weblogic', port=22)
		tp = client.open_sftp()
		tp.get(r"{}/{}".format("/u01/scripts", "jmsCountLog.txt"),
			   r"{}\{}".format(str(self.local_dir), "jmsCountLog.txt"))
		client.close()
		print('file copy is success')

	def print_jms(self):
		str_list = []
		str = ''
		for i in self.strings:
			data, vrem, name_jms, current, pending = i.split(';')
			if int(current) > 70:
				str = data + ' ' + vrem[:-7] + ' ' + name_jms + ' ' + current
				str_list.append(str)
				# Ui_MainWindow.listView.addItem(str)
		print(str_list)
		return str_list

	def time_convert(self, dtime):
		return round(time.mktime(dtime.timetuple()))





if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	sc = SshClient()

 