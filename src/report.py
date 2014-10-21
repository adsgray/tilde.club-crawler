#!/usr/bin/python

# http://zetcode.com/db/sqlitepythontutorial/

import sqlite3 as lite
import sys
import time
from operator import itemgetter

def numusers(con, minsite = 0):
	cur = con.cursor()
	statement = ('select count(*) from user where site_id >= ?')
	data = (str(minsite),)
	cur.execute(statement, data)
	return cur.fetchone()[0]

def topn(con, n, count, minsite = 0):
	cur = con.cursor()
	statement = ('select count(1) cnt, u.name, s.name, s.baseurl from tweet t '
			'inner join user u on u.id = t.user_id '
			'inner join site s on s.id = u.site_id '
			'where t.count >= ? and s.id >= ? group by t.user_id order by cnt DESC limit ?')
	data = (str(count), str(minsite), str(n))
	cur.execute(statement, data)
	return cur.fetchall()


def item_html(item):
	url = "%s/~%s" % (item[3], item[1])
	linktext = "%s/~%s" % (item[2], item[1])
	return """    <li><span class="name">%s</span> <a href="%s">%s</a></li>\n""" % (item[1], url, linktext)

def result_html(arr):
	res = """<ul class="topn">\n"""
	for item in arr:
		res = res + item_html(item)
	res = res + "</ul>\n"
	return res
		

def item_json(item, comma_p):
	"""
	This function is such a freaking mess because JSON does not allow trailing commas.
	It's unreasonable and barbaric.
	"""
	url = "%s/~%s" % (item[3], item[1])
	res = """    {"name" : "%s", "url" : "%s" }""" % (item[1], url)
	if comma_p:
		res = res + ",\n"
	else:
		res = res + "\n"
	return res

def result_json(arr):
	res = "[\n"
	# loop through all but last
	for item in arr[:-1]:
		res = res + item_json(item, True) 
	# now add last element, without a comma THANKS JSON
	res = res + item_json(arr[-1], False)
	res = res + "]"
	return res

def html_report(users, extra_users, topn, extra_topn):
	dt = time.strftime("%c")
	html = """<dl class="count">\n    <dt>Updated</dt><dd>%s</dd>\n    <dt>Total users</dt><dd>%s</dd>\n    <dt>Extra-tilde.club</dt><dd>%s</dd>\n</dl>\n""" % (dt, users, extra_users)
	html += """<h2>Most prolific tilde.club writers</h2>\n"""
	html += result_html(topn)
	html += """<h2>Most prolific Extra-tilde.club writers</h2>\n"""
	html += result_html(extra_topn)
	return html

def json_report(users, extra_users, topn, extra_topn):
	dt = time.strftime("%c")
	json = """{ "updated" : "%s",\n  "total_users" : %s,\n  "extra_tildeclub_users" : %s, \n""" % (dt, users, extra_users)
	json += """  "most_prolific_tildeclub" : %s,\n""" % (result_json(topn))
	json += """  "most_prolific_extra_tildeclub" : %s\n """ % (result_json(extra_topn))
	json += "}\n"
	return json

con = lite.connect('/home/agray/code/db/fortune.db')

try:
	users = numusers(con)
	extra_users = numusers(con, 2)
	# ya, sort by name. don't want a competition
	topn_writers = sorted(topn(con, 15, 0), key=itemgetter(1))
	topn_other_writers = sorted(topn(con, 15, 0, 2), key=itemgetter(1))

	if len(sys.argv) > 1 and sys.argv[1] == "json":
		print json_report(users, extra_users, topn_writers, topn_other_writers)
	else:
		print html_report(users, extra_users, topn_writers, topn_other_writers)

except lite.Error, e:
	print "Error %s:" % e.args[0]
	sys.exit(1)
finally:
	if con:
		con.commit()
		con.close()
