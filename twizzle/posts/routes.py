from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from twizzle.queries import insert_post, get_post_by_id, update_a_post, delete_a_post, like_post, unlike_post, get_like, get_likes_for_post, has_user_liked_post, get_comments_count_by_post_id, add_comment, get_comments_by_post_id
from twizzle.posts.forms import PostForm, CommentForm
from twizzle.models import Post, Comment
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


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = get_post_by_id(post_id)

    like_count = get_likes_for_post(post_id)
    post['likes'] = like_count
    comment_count = get_comments_count_by_post_id(post_id)
    post['comments'] = comment_count

    comments = get_comments_by_post_id(post_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        comment_data = dict(content=form.content.data,
                            uid=current_user.id,
                            pid=post['post_id'])
        comment = Comment(comment_data)
        add_comment(comment)
        flash('Your comment has been created!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))


    return render_template('post.html', title=post['title'], 
                           post=post, comments=comments, form=form)


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
    
    return jsonify({"likes": likes, "liked": liked})


@posts.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = get_post_by_id(post_id)
    if form.validate_on_submit():
        comment_data = dict(content=form.content,
                            uid=current_user.id,
                            pid=post.pid)
        comment = Comment(comment_data)
        add_comment(comment)
        flash('Your comment has been created!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    