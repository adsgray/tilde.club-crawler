# Local tilde.club web crawler

## Purpose
* create a database of text from tilde.club index.html pages
* maybe manually prune them down to 'tweetable' or otherwise high-quality snippets
* set up a twitter bot to tweet quotes along with a link to the corresponding tilde.club page

## Files
* _getusers.pl_ generate SQL to insert user records into sqlite3 db
* _generate\_usermap.sh_ select from db to create map of userid to username
* _local\_crawl.pl_  takes a usermap file and process index.html for each user. Produces an INSERT statement for each sentence on the page. Sentences go into _tweet_ table.
