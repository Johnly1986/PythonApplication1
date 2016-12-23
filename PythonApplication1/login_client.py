import time
import gevent
import dbto
import random
from models import User
import cPickle as pickle
from gevent import socket
from gevent.threadpool import ThreadPool
from socket import AF_INET, SOCK_STREAM, socket

ADDR = ('127.0.0.1' , 8888)
BEGINTIME = int(time.time())
THREAD_NUM = 100

db = dbto.DbTo()
userlist = []

def test(pre, i, tcount):
	count = 0
	if i == 2:
		param = (100)
		sql = "select * from user order by rand() limit %d"%param
		global userlist
		userlist = db.sql_result(sql)
	else:
		pass

	while (count < tcount):
		print 'The count is:', count
		mark = "%s_%d"%(pre, ((BEGINTIME << 16) + count))
		pool = ThreadPool(THREAD_NUM)
		pool.spawn(handle_client, mark, i, gevent.sleep)
		pool.join()
		count = count + 1
	gevent.sleep(1)

def register(client, record):
	pick = pickle.dumps(record)
	client.send(pick)
	return True

def login(client, record):
	pick = pickle.dumps(record)
	client.send(pick)
	return True

def logout(client, record):
	pick = pickle.dumps(record)
	client.send(pick)
	return True

def handle_client(mark, activeIndex, sleep):
	global userlist

	BUFSIZE	= 1024
	ACTIVES = [logout, register, login]
	active = ACTIVES[activeIndex]
	try:
		client = socket(AF_INET, SOCK_STREAM)
		client.connect(ADDR)
		if activeIndex == 2:
			randUserIndex = int(random.random() * len(userlist))
			randUser = userlist[randUserIndex]
			record = {cmd : activeIndex, username : randUser[1], password : randUser[2]}
			result = active(client, record)
		else:
			record = dict(cmd = activeIndex, username = mark, password = "skip")
			result = active(client, record)
		print mark , "active result : " , result
		client.close()
	except Exception as e:
		print "Error ", e
	finally:
		client.close()

def handle_user(client, username):
	pass

if __name__ == '__main__':
	# sqltest()
	import sys
	print sys.path
	if len(sys.argv) == 4:
		test(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
	else:
		test("pre", 0, 1000)