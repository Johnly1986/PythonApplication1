import time
import sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import User

TEST_TIMES = 1000

def test_insert(session):
	count = 0
	while count < TEST_TIMES:
		count += 1
		username = "ti_%d" % (count)
		user = User(name = username, password = '123456')
		session.add(user)
		session.commit()

def test_delete(session):
	count = 0
	while count < TEST_TIMES:
		count += 1
		username = "nti_%d" % (count)
		#user = User(name = username)
		session.query(User).filter(User.name == username).delete()
		session.commit()

def test_update(session):
	count = 0
	while count < TEST_TIMES:
		count += 1
		username = "ti_%d" % (count)
		newusername = "nti_%d" % (count)
		session.query(User).filter(User.name == username).update({'name' : newusername})
		session.commit()

def test_select(session):
	count = 0
	while count < TEST_TIMES:
		count += 1
		username = "nti_%d" % (count)
		user = session.query(User).filter(User.name == username).one()

engine = create_engine('mysql+mysqldb://johnly:123456@localhost:3306/test')
DBSession = sessionmaker(bind=engine)
session = DBSession()

test_list = [test_insert, test_update, test_select, test_delete]

for tfun in test_list:
	print "funtion(", tfun, ") begin time >> "
	print time.time()
	tfun(session)
	print "funtion end time >> ", time.time()

session.close()