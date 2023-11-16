from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bloggy import Bloggy
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt

bcrpyt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrpyt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['id'] = id
    flash("Registration Successful", "success")
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrpyt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['id'] = user.id
    flash("Login Successful", "success")
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    user = User.get_by_id({'id': user_id})

    #likes = likes.get_all_likes()
    if user:
        bloggys = Bloggy.get_bloggys_by_id(user_id)
        likes_dict = {}
        for bloggy in bloggys:
            like_count = len(Like.get_likes_for_bloggy(bloggy.bloggy_id))
            likes_dict[bloggy.bloggy_id] = like_count
        return render_template("dashboard.html", user=user, bloggys=bloggys, likes_dict=likes_dict) #likes=likes
    else: 
        flash("User not found", "error")
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "logged_out")
    return redirect('/')

@app.route('/account/info')
def get_acc_info():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    user = User.get_by_id({'id': user_id})
    
    if user:
        total_bloggys = User.get_total_bloggys(user_id)
        total_likes = Like.get_total_likes_for_user(user_id)
        return render_template("my_account.html", user=user, total_bloggys=total_bloggys, total_likes=total_likes)
    else:
        flash("User not found", "error")
        return redirect('/')
    
@app.route('/feed')
def feed():
    if 'id' not in session:
        return redirect('/logout')
    user_id = session['id']
    users = User.get_all()
    bloggys = Bloggy.get_all_bloggys()

    liked_bloggies = Like.get_liked_bloggys_for_user(user_id)

    likes_dict = {}

    for bloggy in bloggys:
        like_count = len(Like.get_likes_for_bloggy(bloggy.bloggy_id))
        liked = bloggy.bloggy_id in liked_bloggies
        likes_dict[bloggy.bloggy_id] = {'count': like_count,'liked': liked }
        print(like_count)
    return render_template("feed.html", users=users, bloggys=bloggys, likes_dict=likes_dict, user_liked_bloggies=liked_bloggies)

@app.route('/virtual/diary')
def virt_diary():
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': session['id']
    }
    user = User.get_by_id(data)
    bloggys = Bloggy.get_bloggys_by_id(session['id'])
    if user:
        return render_template("virtual_diary.html", user=user, bloggys=bloggys) 
    else: 
        flash("User not found", "error")
        return redirect('/')