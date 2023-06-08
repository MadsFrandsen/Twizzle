from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from twizzle.queries import insert_post, get_post_by_id, update_a_post, delete_a_post, like_post, unlike_post, get_like, get_likes_for_post, has_user_liked_post
from twizzle.posts.forms import PostForm
from twizzle.models import Post
from flask_login import current_user, login_required



posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post_data = dict(title=form.title.data,
                         content=form.content.data,
                         uid=current_user.id)
        post = Post(post_data)
        insert_post(post)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', 
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = get_post_by_id(post_id)
    return render_template('post.html', title=post['title'], post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = get_post_by_id(post_id)
    if post['user_id'] != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post['title'] = form.title.data
        post['content'] = form.content.data
        update_a_post(post)
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post['post_id']))
    elif request.method == 'GET':
        form.title.data = post['title']
        form.content.data = post['content']
    form.title.data = post['title']
    form.content.data = post['content']
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = get_post_by_id(post_id)
    if post['user_id'] != current_user.id:
        abort(403)
    delete_a_post(post_id)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/like/<int:post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = get_post_by_id(post_id)
    like = get_like(current_user.id, post_id)
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        unlike_post(current_user.id, post_id)
    else:
        like_post(current_user.id, post_id)
    likes = get_likes_for_post(post_id)
    liked = has_user_liked_post(current_user.id, post_id)
    
    return jsonify({"likes": likes}, {"liked": liked})