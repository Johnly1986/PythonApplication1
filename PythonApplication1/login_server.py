import sys
import socket
import time
import gevent
import sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cPickle as pickle
from gevent import socket
from models import User, Cache, Item

engine = create_engine('mysql+mysqldb://johnly:123456@localhost:3306/test')
DBSession = sessionmaker(bind=engine)
session = DBSession()

def log(s, addr, cmd):
	cache = Cache(ip = addr, data = cmd, time = int(time.time()))
	session.add(cache)
	session.commit()

def register(username, password):
	user = User(name = username, password = password)
	session.add(user)
	session.commit()
	return True

def has(username, password):
	users = session.query(User).filter(User.name == username).all()
	if len(users) > 0:
		return True
	else:
		return False

def server(port):
	# global db
	# db.get_instance()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0', port))
	s.listen(8888)
	while True:
		cli, addr = s.accept()
		gevent.spawn(handle_request, cli, addr, gevent.sleep)
		gevent.sleep(0)

def handle_request(s, addr, sleep):
	try:
		while True:
			data = s.recv(1024)
			routing(s, addr, data)
			sleep(0)
	except Exception, ex:
		print ex
	finally:
		print 'undo'
		sys.stdout.flush()
		s.close()

def routing(s, addr, data):
	mypack = pickle.loads(data)
	print 'from ', addr, 'recved ', mypack
	cmd = mypack['cmd']
	if cmd == 0:
		s.shutdown(socket.SHUT_WR)
		print s,'.','be killed'
	elif cmd == 1:
		result = register(mypack['username'], mypack['password'])
		sendpack = pickle.dumps(dict(cmd = cmd, result = result))
		s.send(sendpack)
	elif cmd == 2:
		result = has(mypack['username'], mypack['password'])
		sendpack = pickle.dumps(dict(cmd = cmd, result = result))
		s.send(sendpack)
	else:
		request_string = "recved server msg \n"
		s.send(request_string)
		log(s, addr, cmd)

if __name__ == '__main__':
	server(8888)