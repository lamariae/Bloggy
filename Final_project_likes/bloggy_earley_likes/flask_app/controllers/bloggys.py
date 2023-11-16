from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.bloggy import Bloggy
from flask_app.models.user import User
from flask_app.models.like import Like
from datetime import datetime


@app.route('/bloggy/create')
def new_bloggy():
    if 'id' not in session:
        return redirect('/')
    user = User.get_by_id({'id' : session['id']})
    return render_template("create_bloggy.html", user = user)


@app.route('/bloggy/create', methods = ['POST'])
def create_bloggy():
    if 'id' not in session:
        return redirect('/')
    user_id = session['id']
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'created_at': datetime.now(),
        'user_id' : user_id
    }
    if not Bloggy.validate_create_bloggy(request.form):
        return redirect('/bloggy/create')
    Bloggy.save(data)
    flash("Bloggy created successfully.", "create_bloggy")
    return redirect("/dashboard")

@app.route('/bloggy/delete/<int:bloggy_id>', methods = ['POST'])
def delete_bloggy(bloggy_id):
    Bloggy.delete_bloggy(bloggy_id)
    flash("Bloggy deleted successfully.", "delete_bloggy")
    return redirect('/dashboard')

@app.route('/bloggy/update/<int:bloggy_id>', methods = ['POST'])
def update_bloggy(bloggy_id):
    bloggy = Bloggy.get_bloggy_by_id(bloggy_id)
    if bloggy:
        title = request.form.get('title')
        content = request.form.get('content')

        data = {
            'bloggy_id': bloggy_id,
            'title' : title,
            'content' : content
        }

        if not Bloggy.validate_edit_bloggy(data):
            flash('Bloggy title and body must be at least 3 characters')
            data = {
                'id' : session['id']
            }
            user = User.get_by_id(data)
            return render_template('edit_bloggy.html', bloggy=bloggy, user=user)
        
        Bloggy.save_update(data)
        flash("Bloggy updated successfully.", "bloggy_edit")
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')
    
@app.route('/bloggy/edit/<int:bloggy_id>', methods = ['GET'])
def edit_bloggy(bloggy_id):
    bloggy = Bloggy.get_bloggy_by_id(bloggy_id)
    data = {
        'id': session['id']
    }
    user = User.get_by_id(data)
    return render_template('edit_bloggy.html', bloggy=bloggy, user=user)

@app.route('/bloggy/view/<int:bloggy_id>', methods = ['GET'])
def view_bloggy(bloggy_id):
    bloggy = Bloggy.get_bloggy_by_id(bloggy_id)
    data = {
        'id' : session['id']
    }
    user = User.get_by_id(data)
    return render_template('view_bloggy.html', bloggy=bloggy, user=user)