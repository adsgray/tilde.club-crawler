#!/bin/sh

DB=~/code/db/fortune.db
echo 'select id,name from user;' | sqlite3 $DB 
