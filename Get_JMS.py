import re
import paramiko
from datetime import datetime, date, time, timedelta
import time
import threading
import os
import linecache
import sys
import PyQt5.QtWidgets as QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog


class SshClient:
	strings = ''
	local_dir = sys.argv[0][:-10]

	def __init__(self):
		# self.copy_file()
		with open(str(self.local_dir + 'jmsCountLog.txt'), 'r+', encoding='utf-8') as file1:
			self.strings = file1.readlines()

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

class RefreshThread(QtCore.QThread):
	def __init__(self, mainwindow):
		super().__init__()
		self.mainwindow=mainwindow

class ExampleApp(QtWidgets.QMainWindow):
	a=''
	def __init__(self):
		super().__init__()
		self.a = design.Ui_Dialog()
		self.a.setupUi(self)  # Это нужно для инициализации нашего дизайна
		self.a.lineEdit.setText('70')
		self.a.pushButton.clicked.connect(self.get)
		QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(("clicked()"), self.get))
		QtCore.QObject.co

	def thr(self):
		t=threading.Thread(target=self.get)
		t.start()

	def get(self):
		end=0
		sc = SshClient()
		if self.a.checkBox.isChecked():
			print(1)
			while end!=1:
				result = sc.print_jms()
				self.a.listWidget.clear()
				for i in result:
					self.a.listWidget.insertItem(2,'fdg')
				time.sleep(60)
		else:
			self.a.listWidget.clear()
			result = sc.print_jms()
			for i in result:
				self.a.listWidget.insertItem(2, 'fdg')

				# 	time.sleep(5)
		# 	self.a.listWidget.clear()

		# result = sc.print_jms()
		# self.a.listWidget.clear()
		# for i in result:
		# 	self.a.listWidget.insertItem(2, 'fdg')



def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = ExampleApp()  # Создаём объект класса ExampleApp
	window.show()  # Показываем окно
	app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	sc = SshClient()
	main()
# main()  # то запускаем функцию main()
 