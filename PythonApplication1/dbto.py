import MySQLdb


class DbTo:
# global conn
	conn = {}

	def __init__(self):
		print "create Dbto"

	def get_instance(self):
		if not any(self.conn):
			self.conn[0] = MySQLdb.connect(host="localhost", user="root", passwd="", db="test", charset="utf8")
			return self.conn[0]
		else:
			print conn[0]
			return conn[0]

	def sql_execute(self, sql, param):
		myconn = self.get_instance()
		cursor = myconn.cursor()
		n = cursor.execute(sql, param)
		myconn.commit()
		return n

	def sql_result(self, sql):
		myconn = self.get_instance()
		cursor = myconn.cursor()
		cursor.execute(sql)
		return cursor.fetchall()