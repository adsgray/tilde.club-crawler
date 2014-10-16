#!/usr/bin/python

import urllib2
import sqlite3 as lite
import re
import sys

dbpath = '/home/agray/code/db/fortune.db'
user_url = 'http://tilde.town/~sanqui/tildeverse_users.txt'
user_regex = re.compile(r"^http://(.*)/~(\w+)")

def get_users(url):
	"""
	Returns a list of dicts of the form:
	{ 'sitename': ..., 'user': ... }
	"""
	userlist = []
	web = urllib2.urlopen(url)
	for line in web:
		m = user_regex.match(line)
		if m:
			userlist.append({'sitename':m.group(1), 'user':m.group(2)})
	return userlist

# wheee global db variables
con = lite.connect(dbpath)
cur = con.cursor()

def get_site_id_by_name(sitename):
	"""
	return site.id if sitename exists in db
	"""
	find = ('select id from site where name=?');
	data = (sitename,) # N.B. the comma to turn it into a tuple, or something.
	cur.execute(find, data)
	res = cur.fetchone()
	if not res == None:
		return res[0]
	else:
		return None


def user_in_db(user):
	"""
	predicate: return true if user in db already, false otherwise
	"""
	find = ('select u.id from user as u inner join site as s on (u.site_id = s.id) where u.name = ? and s.name = ?');
	data = (user['user'], user['sitename'])
	cur.execute(find, data)
	return cur.fetchone() != None


def add_user_to_db(user):
	"""
	Add this user to the db
	"""
	if not user_in_db(user):
		siteid = get_site_id_by_name(user['sitename'])
		if not siteid == None:
			add = ('INSERT INTO user (site_id, name) values(?,?)')
			data = (siteid, user['user'])
			cur.execute(add, data)
		else:
			print "cannot find site %s" % (user['sitename'])


def add_users_to_db(userlist):
	"""
	Adds each user to the db if they are not already present
	"""
	for user in userlist:
		add_user_to_db(user)


add_users_to_db(get_users(user_url))

con.commit()
con.close()
