from app import app, db
from app.models import Book
from flask import render_template, flash, redirect, url_for
from app.forms import AddBookForm

@app.route('/')
@app.route('/index')
def index():
    books = Book.query.all()
    return render_template('index.html', title='Home', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data)
        db.session.add(book)
        db.session.commit()
        flash('Congratulations, you have added a new book!')
        return redirect(url_for('index'))
    return render_template('add_book.html', title='Add Book', form=form)
