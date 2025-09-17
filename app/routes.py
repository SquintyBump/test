from app import app, db
from app import torznab
from app import qbittorrent
from app.models import Book, Indexer, DownloadClient
from flask import render_template, flash, redirect, url_for, request
from app.forms import AddBookForm, IndexerForm, SearchForm, DownloadClientForm

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


@app.route('/download_clients')
def download_clients():
    all_clients = DownloadClient.query.all()
    return render_template('download_clients.html', title='Download Clients', clients=all_clients)


@app.route('/add_download_client', methods=['GET', 'POST'])
def add_download_client():
    form = DownloadClientForm()
    if form.validate_on_submit():
        client = DownloadClient(name=form.name.data,
                                host=form.host.data,
                                port=form.port.data,
                                username=form.username.data,
                                password=form.password.data)
        db.session.add(client)
        db.session.commit()
        flash('New download client has been added!')
        return redirect(url_for('download_clients'))
    return render_template('add_download_client.html', title='Add Download Client', form=form)


@app.route('/send_to_client', methods=['POST'])
def send_to_client():
    download_link = request.form.get('link')
    query = request.form.get('query')
    if not download_link or not query:
        flash('Invalid request.')
        return redirect(url_for('search'))

    # This is a simplification; a real app might need a more robust way to link a result to a book
    book = Book.query.filter_by(title=query).first()
    if not book:
        flash(f"Could not find a wanted book with the title: {query}")
        return redirect(url_for('search'))

    client_config = DownloadClient.query.first()
    if not client_config:
        flash('No download client configured.')
        return redirect(url_for('download_clients'))

    download_hash = qbittorrent.add_download(
        host=client_config.host,
        port=client_config.port,
        username=client_config.username,
        password=client_config.password,
        link=download_link
    )

    if download_hash:
        book.status = 'downloading'
        book.download_id = download_hash
        db.session.commit()
        flash(f"Download for '{book.title}' successfully sent to qBittorrent!")
    else:
        flash('Failed to send download to qBittorrent.')

    return redirect(url_for('search'))
