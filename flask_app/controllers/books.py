from flask_app import app
from flask_app import Flask, render_template, request, redirect, session, flash, bcrypt
from flask_app.models import user, book





@app.route('/book/create', methods=['POST'])
def create_new_book():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    if not book.Book.validate_form(request.form):
        return redirect('/magazine/new')

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    book.Book.create_book(data)
    return redirect('/dashboard')

@app.route('/book/favorite', methods=['POST'])
def add_favorite_book():
    book.Book.favorite(request.form)
    return redirect('/dashboard')

@app.route('/book/new')
def book_new():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': session['id'] }
    return render_template('new.html', user=user.User.get_user_by_id(data))

@app.route('/book/show/<int:book_id>')
def book_show_one(book_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': book_id }
    data_user = { 'id': session['id'] }
    return render_template('show.html', one_book=book.Book.get_one_book(data), user=user.User.get_user_by_id(data_user))


@app.route('/book/edit/<int:book_id>')
def edit_book(book_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': book_id }
    data_user = { 'id': session['id'] }

    return render_template('edit.html', one_book=book.Book.get_one_book(data), user=user.User.get_user_by_id(data_user))

@app.route('/book/update', methods=['POST'])
def update_book():
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    if not book.book.validate_form(request.form):
        id = int(request.form['id'])
        return redirect(f'/magazine/edit/{id}')

    data = {
        'id': int(request.form['id']),
        'title': request.form['title'],
        'description': request.form['description'],
    }
    book.Book.update_book(data)
    return redirect('/dashboard')

@app.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': book_id }
    book.Book.delete_book(data)
    return redirect('/dashboard')

@app.route('/book/unfavorite', methods=['POST'])
def un_favorite_book():
    book.Book.unfavorite(request.form)
    return redirect('/dashboard')