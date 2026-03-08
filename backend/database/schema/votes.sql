CREATE TABLE votes(
	user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
	post_id BIGINT REFERENCES posts(id) ON DELETE CASCADE,
	vote_type SMALLINT CHECK (vote_type IN (1,-1)),
	PRIMARY KEY (user_id, post_id)
);