#!/usr/bin/python

import urllib2
from HTMLParser import HTMLParser
import json
from re import sub
import sqlite3 as lite
import sys

dbpath = '/home/agray/code/db/fortune.db'

# http://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def get_text_from_stream(stream):
	parser = _DeHTMLParser();

	try:
		for line in stream:
			parser.feed(line)
	except:
		return parser.text()
	finally:
		return parser.text()


def get_sentences_from_text(text):
	return text.split('. ');

def get_sentences_from_stream(stream):
	return get_sentences_from_text(get_text_from_stream(stream))


def add_sentences_for_user(con, sentences, userid):
	cur = con.cursor()
	for s in sentences:
            	s = sub('[ \t\r\n]+', ' ', s)
		add_tweet = ("INSERT INTO tweet (user_id, text) VALUES(?, ?)")
		tweet_data = (userid, s)
		cur.execute(add_tweet, tweet_data)


def process_user(con, url, userid):
	try:
		web = urllib2.urlopen(url)
		sentences = get_sentences_from_stream(web)
		add_sentences_for_user(con, sentences, userid)
	except Exception as e:
		print "Error %s:" % e
		return
	

def process_all_users():
	try:
		con = lite.connect(dbpath)
		con.text_factory = str
		cur = con.cursor()
		cur.execute('select s.baseurl,u.name,u.id from site as s inner join user as u on u.site_id = s.id');

		rows = cur.fetchall()
		#random.shuffle(rows)

		for row in rows:
			try:
				url = row[0].encode('utf-8') + '/~' + row[1].encode('utf-8')
				process_user(con, url, row[2])
			except UnicodeDecodeError:
				print "could not construct url from: " + str(row)
				continue

	except lite.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:
		if con:
			con.commit()
			con.close()


process_all_users()

