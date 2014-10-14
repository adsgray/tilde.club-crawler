# tilde.club web crawler and tweeter

## Purpose
* create a database of text from tilde.club (and other .club) home pages
* maybe manually prune them down to 'tweetable' or otherwise high-quality snippets
* set up a twitter bot to tweet quotes along with a link to the corresponding tilde.club page

## Files
* _getusers.pl_ generate SQL to insert user records into sqlite3 db
* _generate\_usermap.sh_ select from db to create map of userid to username
* _local\_crawl.pl_  takes a usermap file and process index.html for each user. Produces an INSERT statement for each sentence on the page. Sentences go into _tweet_ table. (DEPRECATED)
* _crawl.py_ fetches and parses user pages and inserts sentences into _tweet_ table
* _tweet.py_ Does not actually tweet. Chooses a random row from _tweet_ table, marks it as used, and prints out a constructed tweet that includes link to originating page.
* _tweet_tilde_quote_ a shell script that takes the output of _tweet.py_ and tweets it out. This is called from cron.

## TODO
* add other ~sites
* make crawl.py smart enough to only process recently updated pages (fetch the .JSON file)
* add crawl.py to cron once it is smart enough.
