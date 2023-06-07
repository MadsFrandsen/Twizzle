from flask import render_template, request, abort, Blueprint
from twizzle.queries import get_some_posts, get_total_posts_count


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
    pages = [i for i in range(1, total_pages+1)]
    return render_template('home.html', posts=posts, page=page, total_pages=total_pages, pages=pages, total_posts=total_posts['count'])


@main.route("/about")
def about():
    return render_template('about.html', title='About')







