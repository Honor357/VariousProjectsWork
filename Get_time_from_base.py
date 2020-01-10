import os
import re
import sys
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import cx_Oracle
import global_name
import paramiko
import time
from xlwt import Workbook, XFStyle, Borders, Font


class ReadSqlAndWriteF(object):
	datB = str(datetime.datetime.strptime(sys.argv[1], '%d.%m.%Y %H:%M:%S'))
	datE = str(datetime.datetime.strptime(sys.argv[2], '%d.%m.%Y %H:%M:%S'))
	path = sys.argv[3]

	Q_Time = """
select 
t.TRX_TYPE, 
t.SYS_EXEC_DEB, 
t.SYS_EXEC_CRED, 
(SUBSTR(numtodsinterval(avg(((extract(day from t.diff)*24 + extract(hour from t.diff))*60 + extract(minute from t.diff))*60 + extract(second from t.diff)), 'second'),12,8) || ',' ||
SUBSTR(numtodsinterval(avg(((extract(day from t.diff)*24 + extract(hour from t.diff))*60 + extract(minute from t.diff))*60 + extract(second from t.diff)), 'second'),21,3)) as avg_trans,
(SUBSTR(max(t.diff),12,8) || ',' || SUBSTR(max(t.diff),21,3)) as max_trans_time,
(SUBSTR(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY t.diff ASC),12,8) || ',' || SUBSTR(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY t.diff ASC),21,3)) as percentile
from
(
SELECT
  ID,
  TRX_TYPE,
  SYS_EXEC_DEB,
  SYS_EXEC_CRED,
  (TO_TIMESTAMP(to_char(DATE_LAST_ACTION,'YYYY-MM-DD HH24:MI:SS.FF6'), 'YYYY-MM-DD HH24:MI:SS.FF6')-TO_TIMESTAMP(to_char(DATE_REG_OP_TS,'YYYY-MM-DD HH24:MI:SS.FF6'), 'YYYY-MM-DD HH24:MI:SS.FF6')) diff
FROM
  prod_tsruntime.transactions
WHERE  date_reg_op_ts > to_date('"""
	Q_Time += datB
	Q_Time += """','yyyy-mm-dd HH24:MI:SS')
			AND date_reg_op_ts < to_date('"""
	Q_Time += datE
	Q_Time += """','yyyy-mm-dd HH24:MI:SS')
			/* AND ID<'TS.0000000017306538'*/
			GROUP BY
			ID,
			TRX_TYPE,
			SYS_EXEC_DEB,
			SYS_EXEC_CRED,
			DATE_REG_OP_TS, 
			DATE_LAST_ACTION,
			TRX_STATUS
			order by id) t 
			group by t.TRX_TYPE, t.SYS_EXEC_DEB, t.SYS_EXEC_CRED
			order by t.TRX_TYPE, t.SYS_EXEC_DEB, t.SYS_EXEC_CRED"""

	Q_Count = """
			select 
			t.TRX_TYPE, 
			t.SYS_EXEC_DEB, 
			t.SYS_EXEC_CRED, 
			t.TRX_STATUS,
			count(t.TRX_STATUS) as COUNT_TRX_STATUS
			from
			(
			SELECT
			  ID,
			  TRX_TYPE,
			  SYS_EXEC_DEB,
			  SYS_EXEC_CRED,
			  TRX_STATUS
			FROM
			  prod_tsruntime.transactions
			WHERE 
			date_reg_op_ts > to_date('"""
	Q_Count += datB
	Q_Count += """','yyyy-mm-dd HH24:MI:SS')
			AND date_reg_op_ts < to_date('"""
	Q_Count += datE
	Q_Count += """','yyyy-mm-dd HH24:MI:SS')
			/* AND ID<'TS.0000000017306538'*/
			GROUP BY
			ID,
			TRX_TYPE,
			SYS_EXEC_DEB,
			SYS_EXEC_CRED,
			TRX_STATUS
			order by id) t 
			group by t.TRX_TYPE, t.SYS_EXEC_DEB, t.SYS_EXEC_CRED, t.TRX_STATUS
			order by t.TRX_TYPE, t.SYS_EXEC_DEB, t.SYS_EXEC_CRED, t.TRX_STATUS"""

	def __init__(self, *args):
		print(sys.argv)
		print(sys.argv[1])
		self.datB = str(datetime.datetime.strptime(sys.argv[1], '%d.%m.%Y %H:%M:%S'))
		self.datE = str(datetime.datetime.strptime(sys.argv[2], '%d.%m.%Y %H:%M:%S'))
		self.path = sys.argv[3]

	def connect_sql_and_write_xlsx(self, num):
		dsn = cx_Oracle.makedsn(global_name.oracle_host, global_name.oracle_port, global_name.oracle_sid)
		conn = cx_Oracle.connect(global_name.oracle_user, global_name.oracle_password, dsn)
		cursor = conn.cursor()  #подключение
		cursor.execute(self.Q_Count) #выполнение запроса
		self.write_cursor_to_excel(cursor, self.path + '\\Count_' + num + '.xls', 'Count_transaction', 'Count')
		cursor.execute(self.Q_Time)
		self.write_cursor_to_excel(cursor, self.path + '\\Time_' + num + '.xls', 'Time_of_transaction', 'Time')
		cursor.close()

	def write_cursor_to_excel(self, curs, filename, sheetTitle, type_sql):

		## -- write_cursor_to_excel  curs: a cursor for an open connection to an oracle database
		## -- filename: name of the XLS file to create sheetTitle: name of the sheet to create
		## -- create style for header row - bold font, thin border below
		fnt = Font()
		fnt.bold = True
		borders = Borders()
		borders.bottom = Borders.THIN
		hdrstyle = XFStyle()
		hdrstyle.font = fnt
		hdrstyle.borders = borders
		# create a date format style for any date columns, if any
		datestyle = XFStyle()
		datestyle.num_format_str = 'DD/MM/YYYY'
		# create the workbook. (compression: try to reduce the number of repeated styles)
		wb = Workbook(style_compression=2)
		# the workbook will have just one sheet
		sh = wb.add_sheet(sheetTitle)
		sh1 = wb.add_sheet('Sql')
		# write the header line, based on the cursor description
		c = 0
		colWidth = []
		for col in curs.description:
			# col[0] is the column name
			# col[1] is the column data type
			sh.write(0, c, col[0], hdrstyle)
			colWidth.append(1)  # arbitrary min cell width
			if col[1] == cx_Oracle.DATETIME:
				colWidth[-1] = len(datestyle.num_format_str)
			if colWidth[-1] < len(col[0]):
				colWidth[-1] = len(col[0])
			c += 1
		# write the songs, one to each row
		r = 1
		for song in curs:
			row = sh.row(r)
			for c in range(len(song)):
				if song[c]:
					if curs.description[c][1] == cx_Oracle.DATETIME:
						row.write(c, song[c], datestyle)
					else:
						if colWidth[c] < len(str(song[c])):
							colWidth[c] = len(str(song[c]))
						row.write(c, song[c])
			r += 1
		for c in range(len(colWidth)):
			sh.col(c).width = colWidth[c] * 350
		# freeze the header row
		sh.panes_frozen = True
		sh.vert_split_pos = 0
		sh.horz_split_pos = 1

		sh1.col(c).width = 700
		sh1.col(c).height = 1200
		for c in range(len(colWidth)):
			sh.col(c).width = colWidth[c] * 350
			if type_sql == 'Time':
				sh1.write(0, c, self.Q_Time, hdrstyle)
			else:
				sh1.write(0, c, self.Q_Count, hdrstyle)

		wb.save(filename)


if __name__ == "__main__":
	main = ReadSqlAndWriteF()
	main.connect_sql_and_write_xlsx(sys.argv[4])
