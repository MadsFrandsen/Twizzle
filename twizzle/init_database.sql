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
    like_id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER,
    post_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    UNIQUE (user_id, post_id)
);

CREATE INDEX IF NOT EXISTS likes_index
ON Likes(like_id, user_id, post_id);


COPY Users(email_address, user_name, password)
FROM '/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/only_hashed.csv'
DELIMITER ','
CSV HEADER;

COPY Posts(title, content, user_id)
FROM '/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/post_data.csv'
DELIMITER ','
CSV HEADER;


/*id SERIAL not null PRIMARY KEY,*/