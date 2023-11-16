from flask import render_template, request, redirect, session, flash, url_for, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bloggy import Bloggy
from flask_app.models.like import Like
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

@app.route('/like/<int:bloggy_id>', methods=['POST'])
def like_bloggy(bloggy_id):
    print(f"Like bloggy route triggered for bloggy_id: {bloggy_id}")
    if 'id' not in session:
        flash("You must be logged in to like a bloggy.", "error")
        return redirect('/login')  

    user_id = session['id']

    existing_like = Like.get_like_by_user_and_bloggy(user_id, bloggy_id)

    if existing_like:
        Like.unlike({'user_id': user_id, 'bloggy_id': bloggy_id})
        flash("You unliked the bloggy.", "unlike_bloggy")
    else:
        Like.save_like({'user_id': user_id, 'bloggy_id': bloggy_id})
        flash("You liked the bloggy.", "like_bloggy")
    
    like_count = len(Like.get_likes_for_bloggy(bloggy_id))
    return {'liked' : not existing_like, 'likeCount' : like_count}