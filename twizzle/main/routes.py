from flask import render_template, request, abort, Blueprint
from twizzle.queries import get_some_posts, get_total_posts_count, get_likes_for_post, has_user_liked_post, get_comments_count_by_post_id, recommend_followers, get_user_by_id
from flask_login import current_user


main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    total_posts = get_total_posts_count()
    limit = 5
    total_pages = (total_posts['count'] + limit) // limit

    if page < 1 or page > total_pages:
        abort(404)

    offset = (page - 1) * limit
    posts = get_some_posts(offset, limit)

    for post in posts:
        likes_count = get_likes_for_post(post['post_id'])
        post['likes'] = likes_count
        comment_count = get_comments_count_by_post_id(post['post_id'])
        post['comments'] = comment_count
        if current_user.is_authenticated:
            has_liked = has_user_liked_post(current_user.id, post['post_id'])
            post['liked'] = has_liked
    

    rec_followers = {}
    if current_user.is_authenticated:
        rec_followers = recommend_followers(current_user.id)
        for rec_follow in rec_followers:
            user = get_user_by_id(rec_follow['user_id1'])
            rec_follow['user_name'] = user.user_name
            rec_follow['image_file'] = user.image_file
     

    pages = [i for i in range(1, total_pages+1)]
    return render_template('home.html', posts=posts, page=page, 
                           total_pages=total_pages, pages=pages, 
                           total_posts=total_posts['count'],
                           rec_followers=rec_followers)


@main.route("/about")
def about():
    return render_template('about.html', title='About')







