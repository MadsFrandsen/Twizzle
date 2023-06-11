DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
    user_id SERIAL NOT NULL PRIMARY KEY,
    email_address VARCHAR(255) UNIQUE,
    user_name VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    image_file TEXT DEFAULT 'default.jpg'
);

CREATE INDEX IF NOT EXISTS users_index
ON Users(user_id, email_address);

DELETE FROM Users;


DROP TABLE IF EXISTS Posts CASCADE;

CREATE TABLE IF NOT EXISTS Posts(
    post_id SERIAL NOT NULL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    post_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE INDEX IF NOT EXISTS posts_index
ON Posts(post_id, user_id);

DELETE FROM Posts;

DROP TABLE IF EXISTS Likes CASCADE;

CREATE TABLE IF NOT EXISTS Likes(
    user_id INTEGER,
    post_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    PRIMARY KEY (user_id, post_id)
);


DROP TABLE IF EXISTS Follows CASCADE;

CREATE TABLE IF NOT EXISTS Follows(
    user_id1 INTEGER,
    user_id2 INTEGER,
    FOREIGN KEY (user_id1) REFERENCES Users(user_id),
    FOREIGN KEY (user_id2) REFERENCES Users(user_id),
    PRIMARY KEY (user_id1, user_id2)
);


DROP TABLE IF EXISTS Comments CASCADE;

CREATE TABLE IF NOT EXISTS Comments(
    comment_id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER,
    post_id INTEGER,
    content TEXT,
    comment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);



