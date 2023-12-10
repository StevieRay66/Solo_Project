# Import app
from flask_app import app
from flask_app import Flask, render_template, request, redirect, session, flash, bcrypt
from flask_app.models.user import User
from flask_app.models import user, book

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user_info = request.form
    if not User.is_valid_user(user_info):
        return redirect ('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """Welcome page"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = {
        'id': session['id']
    }

    one_user = user.User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name

    all_books = book.Book.get_all_books()
    print(all_books)
    return render_template('dashboard.html', one_user=one_user, all_books=all_books)

@app.route('/user/account')
def display_user_acct():
    """Display user account to update"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    data = {
        'id': session['id']
    }

    one_user = user.User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name

    all_books = book.Book.get_all_books()
    return render_template('account.html', one_user=one_user, all_books=all_books)

@app.route('/user/account/update', methods=['POST'])
def user_update():
    """Update the user info"""

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    if not user.User.validate_account(request.form):
        return redirect(f'/user/account')
    data = {
        'id': session['id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    user.User.update_user(data)

    flash("Success! Your info has changed", "success")
    return redirect('/user/account')

@app.route('/login', methods=['POST'])
def login():
    """Login in the user"""
    data = { 'email': request.form['email'] }
    user_in_db = user.User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email or Need to register", "danger")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("The password must match and be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


