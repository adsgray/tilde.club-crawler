-- tilde.club users. 
create table user(
	id INTEGER PRIMARY KEY,
	name varchar(100)
);


create table tweet(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	text varchar(1000) NOT NULL UNIQUE,
	count INTEGER DEFAULT 0,
	FOREIGN KEY(user_id) REFERENCES user(id)
);
