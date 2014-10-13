-- tilde.club users. 
create table user(
	id INTEGER PRIMARY KEY,
	name varchar(100)
);


create table tweet(
	-- id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	text varchar(160) NOT NULL,
	count INTEGER DEFAULT 0,
	PRIMARY KEY (user_id, text)
	FOREIGN KEY(user_id) REFERENCES user(id)
);
