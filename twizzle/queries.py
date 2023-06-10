from twizzle import cur, conn
from twizzle.models import User, Post, Comment
from flask import abort


def insert_user(user: User):
    sql ="""
    INSERT INTO Users(email_address, user_name, password)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (user.email_address, user.user_name, user.password))
    conn.commit()


def init_user(email_address, user_name, password):
    sql ="""
    INSERT INTO Users(email_address, user_name, password)
    VALUES (%s, %s, %s)
    """
    # cur.execute(sql, (user['email_address'], user['user_name'], user['password']))
    cur.execute(sql, (email_address, user_name, password))
    conn.commit()


def insert_post(post: Post):
    sql = """
    INSERT INTO Posts(title, content, user_id)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (post.title, post.content, post.uid))
    conn.commit()


def get_user_by_name(user_name):
    sql = """
    SELECT *
    FROM Users
    WHERE user_name = %s
    """
    cur.execute(sql, (user_name,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    return user


def get_user_by_email(email):
    sql = """
    SELECT *
    FROM Users
    WHERE email_address = %s
    """
    cur.execute(sql, (email,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    return user

def get_user_by_id(id):
    sql = """
    SELECT *
    FROM Users
    WHERE user_id = %s
    """
    cur.execute(sql, (id,))
    user = User(cur.fetchone()) if cur.rowcount > 0 else None
    return user


def get_all_posts():
    sql = """
    SELECT P.post_id, P.title, P.content, P.post_date, U.user_name, U.image_file
    FROM Posts P
    JOIN Users U ON P.user_id = U.user_id
    """
    cur.execute(sql)
    posts = cur.fetchall()
    return posts


def get_some_posts(offset, limit):
    sql = """
    SELECT P.post_id, P.title, P.content, P.post_date, U.user_name, U.image_file
    FROM Posts P
    JOIN Users U ON P.user_id = U.user_id
    ORDER BY P.post_date DESC
    OFFSET %s LIMIT %s
    """
    cur.execute(sql, (offset, limit))
    posts = cur.fetchmany(limit)
    return posts


def get_total_posts_count():
    sql = """
    SELECT COUNT(*)
    FROM Posts
    """
    cur.execute(sql)
    count = cur.fetchone()
    return count


def get_some_posts_by_user(user: User, offset, limit):
    sql = """
    SELECT P.post_id, P.title, P.content, P.post_date, U.user_name, U.image_file
    FROM Posts P, Users U
    WHERE P.user_id = U.user_id AND P.user_id = %s
    ORDER BY P.post_date DESC
    OFFSET %s LIMIT %s
    """
    cur.execute(sql, (user.id, offset, limit))
    posts = cur.fetchmany(limit)
    return posts


def get_user_post_count(user: User):
    sql = """
    SELECT COUNT(*)
    FROM Posts P
    WHERE P.user_id = %s
    """
    cur.execute(sql, (user.id,))
    count = cur.fetchone()
    return count


def get_post_by_id(id):
    sql = """
    SELECT P.post_id, P.user_id, P.title, P.content, P.post_date, U.user_name, U.image_file
    FROM Posts P
    JOIN Users U ON P.post_id = %s AND P.user_id = U.user_id
    """
    cur.execute(sql, (id,))
    post = cur.fetchone() if cur.rowcount > 0 else abort(404)
    return post


def update_user_info(user: User):
    sql = """
    UPDATE Users
    SET email_address = %s,
    user_name = %s,
    image_file = %s
    WHERE user_id = %s
    """
    cur.execute(sql, (user.email_address, user.user_name, user.image_file, user.id))
    conn.commit()


def update_a_post(post: dict):
    sql = """
    UPDATE Posts
    SET title = %s,
    content = %s
    WHERE post_id = %s
    """
    cur.execute(sql, (post['title'], post['content'], post['post_id']))
    conn.commit()


def update_user_password(user: User):
    sql = """
    UPDATE Users
    SET password = %s
    WHERE user_id = %s
    """
    cur.execute(sql, (user.password, user.id))
    conn.commit()


def delete_a_post(id):
    sql = """
    DELETE FROM Posts
    WHERE post_id = %s
    """
    cur.execute(sql, (id,))
    conn.commit()


def like_post(user_id, post_id):
    sql = """
    INSERT INTO Likes(user_id, post_id)
    VALUES (%s, %s)
    """
    cur.execute(sql, (user_id, post_id))
    conn.commit()


def unlike_post(user_id, post_id):
    sql = """
    DELETE FROM Likes
    WHERE user_id = %s AND post_id = %s
    """
    cur.execute(sql, (user_id, post_id))
    conn.commit()


def get_like(user_id, post_id):
    sql = """
    SELECT *
    FROM Likes
    WHERE user_id = %s AND post_id = %s
    """
    cur.execute(sql, (user_id, post_id))
    like = cur.fetchone() if cur.rowcount > 0 else None
    return like


def get_likes_for_post(post_id):
    sql = """
    SELECT COUNT(*) as like_count
    FROM Likes
    WHERE post_id = %s
    """
    cur.execute(sql, (post_id,))
    count = cur.fetchone()
    like_count = count['like_count']
    return like_count


def has_user_liked_post(user_id, post_id):
    sql = """
    SELECT *
    FROM Likes
    WHERE user_id = %s AND post_id = %s
    """
    cur.execute(sql, (user_id, post_id))
    return True if cur.rowcount > 0 else False


def add_comment(user_id, post_id, content):
    sql = """
    INSERT INTO Comments(user_id, post_id, content)
    VALUES(%s, %s, %s)
    """
    cur.execute(sql, (user_id, post_id, content))
    conn.commit()


def delete_comment(comment_id):
    sql = """
    DELETE FROM Comments
    WHERE comment_id = %s
    """
    cur.execute(sql, (comment_id,))
    conn.commit()


def get_comments_by_post_id(post_id):
    sql = """
    SELECT *
    FROM Comments
    WHERE post_id = %s
    """
    cur.execute(sql, (post_id))
    comments = cur.fetchall()
    return comments

<<<<<<< HEAD
def recommend_followers(user_id):
    sql = """
    select user_id2 from
    (select user_id2, count(user_id2)from follows_test 
    where user_id1 !=%s and user_id1 in (select user_id2 from follows_test where user_id1 = %s) 
    group by user_id2 having count(user_id2)>1) as finnal order by count desc;
    """
    cur.execute(sql, (user_id))
    comments = cur.fetchall()
    return comments

    
=======

def get_followers_count_for_user(user_id):
    sql = """
    SELECT COUNT(*) as follower_count
    FROM Follows
    WHERE user_id1 = %s
    """
    cur.execute(sql, (user_id,))
    count = cur.fetchone()
    follow_count = count['follower_count']
    return follow_count


def get_following_count_for_user(user_id):
    sql = """
    SELECT COUNT(*) as following_count
    FROM Follows
    WHERE user_id2 = %s
    """
    cur.execute(sql, (user_id,))
    count = cur.fetchone()
    following_count = count['following_count']
    return following_count


def follow_user(user_id1, user_id2):
    sql = """
    INSERT INTO Follows(user_id1, user_id2)
    VALUES(%s, %s)
    """
    cur.execute(sql, (user_id1, user_id2))
    conn.commit()


def unfollow_user(user_id1, user_id2):
    sql = """
    DELETE FROM Follows
    WHERE user_id1 = %s AND user_id2 = %s
    """
    cur.execute(sql, (user_id1, user_id2))
    conn.commit()


def does_user_follow(user_id1, user_id2):
    sql = """
    SELECT *
    FROM Follows
    WHERE user_id1 = %s AND user_id2 = %s
    """
    cur.execute(sql, (user_id1, user_id2))
    return True if cur.rowcount > 0 else False
>>>>>>> 5daf29a4256a739d7a40cec07403ce7bdbfbeb1a
