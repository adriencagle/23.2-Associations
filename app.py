"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db,  Users, connect_db, Post

# create_app()
app = Flask(__name__)

config = app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()


@app.route('/')
def root():

    return redirect('/users')

@app.route('/users')
def users_index():
    users = Users.query.order_by(Users.lastname, Users.firstname).all()
    return render_template('/index.html', users = users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    return render_template('/new.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    new_user_info = Users(
        firstname = request.form['firstname'],
        lastname = request.form['lastname'],
        img_url = request.form['img_url'] or None
    )

    db.session.add(new_user_info)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(users_id):
    user = Users.query.get_or_404(users_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:users_id>/edit')
def users_edit(users_id):
    user = Users.query.get_or_404(users_id)
    return render_template('users/edit.html', user = user)

@app.route('/users/<int:users_id>/edit', methods=["POST"])
def users_update(users_id):
    user = Users.query.get_or_404(users_id)
    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:users_id>/delete', methods=["POST"])
def users_delete(users_id):
    user = Users.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    user = Users.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
