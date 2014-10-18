#!/usr/bin/python

# http://zetcode.com/db/sqlitepythontutorial/

import sqlite3 as lite
import sys
import random
from subprocess import call


def get_random_tweets(con, num, min_site):
	cur = con.cursor()
	cur.execute('select t.id,t.text,u.name,s.baseurl from tweet as t inner join user as u on (u.id = t.user_id) inner join site as s on (s.id = u.site_id) where LENGTH(t.text) < 118 AND t.count=0 AND s.id >= %s;' % (min_site));
	
	rows = cur.fetchall()
	random.shuffle(rows)
	
	chosen = rows[0:num];
	#for tweet in chosen:
		#print tweet
	return chosen


def mark_as_used(con, tweets):
	cur = con.cursor()
	for tweet in tweets:
		cur.execute('update tweet set count=1 where id=' + str(tweet[0]))
	

def construct_tweet_strings(tweets):
	arr = []
	for tweet in tweets:
		arr.append('"{0}" {1}/~{2}'.format(tweet[1], tweet[3], tweet[2]))
	return arr

def fire_tweets(tweets):
	for tweet in tweets:
		print tweet
		

con = lite.connect('/home/agray/code/db/fortune.db')

try:
	if len(sys.argv) == 2:
		min_site = sys.argv[1]
	else:
		min_site = 1
	tweets = get_random_tweets(con, 1, min_site)
	tweet_strings = construct_tweet_strings(tweets)
	fire_tweets(tweet_strings)
	mark_as_used(con, tweets)
except lite.Error, e:
	print "Error %s:" % e.args[0]
	sys.exit(1)
finally:
	if con:
		con.commit()
		con.close()
