
create table site(
	id INTEGER PRIMARY KEY,
	name varchar(100),
	baseurl varchar(100),
	recentmodpath varchar(100)
);

-- tilde.club and affiliated users. 
create table user(
	id INTEGER PRIMARY KEY,
	site_id INTEGER,
	name varchar(100),
	FOREIGN KEY(site_id) REFERENCES site(id)
);


create table tweet(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	text varchar(1000) NOT NULL UNIQUE,
	count INTEGER DEFAULT 0,
	FOREIGN KEY(user_id) REFERENCES user(id)
);
