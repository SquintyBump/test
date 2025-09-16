from app import app, db
from app import torznab
from app.models import Book, Indexer
from flask import render_template, flash, redirect, url_for
from app.forms import AddBookForm, IndexerForm, SearchForm

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


@app.route('/indexers')
def indexers():
    all_indexers = Indexer.query.all()
    return render_template('indexers.html', title='Indexers', indexers=all_indexers)


@app.route('/add_indexer', methods=['GET', 'POST'])
def add_indexer():
    form = IndexerForm()
    if form.validate_on_submit():
        indexer = Indexer(name=form.name.data, url=form.url.data, api_key=form.api_key.data)
        db.session.add(indexer)
        db.session.commit()
        flash('New indexer has been added!')
        return redirect(url_for('indexers'))
    return render_template('add_indexer.html', title='Add Indexer', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.query.data
        all_indexers = Indexer.query.all()
        for indexer in all_indexers:
            indexer_results = torznab.search(indexer.url, indexer.api_key, query)
            results.extend(indexer_results)
    return render_template('search.html', title='Search', form=form, results=results)
