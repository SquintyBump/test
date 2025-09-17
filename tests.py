import unittest
from unittest.mock import patch
from app import app, db, jobs
from app.models import Book, Indexer, DownloadClient

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_book(self):
        # test adding a book
        response = self.app.post('/add_book', data=dict(
            title='The Lord of the Rings',
            author='J.R.R. Tolkien'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # check that the book was added to the database
        book = Book.query.get(1)
        self.assertIsNotNone(book)
        self.assertEqual(book.title, 'The Lord of the Rings')

    def test_index_page(self):
        # test that the index page loads
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)

        # test that a book added previously is on the index page
        b = Book(title='The Hobbit', author='J.R.R. Tolkien')
        db.session.add(b)
        db.session.commit()
        response = self.app.get('/index')
        self.assertIn(b'The Hobbit', response.data)


class IndexerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_indexer(self):
        # test adding an indexer
        response = self.app.post('/add_indexer', data=dict(
            name='Test Indexer',
            url='http://test.indexer.com',
            api_key='12345'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # check that the indexer was added to the database
        indexer = Indexer.query.get(1)
        self.assertIsNotNone(indexer)
        self.assertEqual(indexer.name, 'Test Indexer')

    @patch('app.torznab.search')
    def test_search(self, mock_search):
        # Configure the mock to return a fake result
        mock_search.return_value = [{'title': 'Fake Book Title', 'link': 'http://fake.link'}]

        # Add a test indexer to the database
        indexer = Indexer(name='Test Indexer', url='http://test.indexer.com', api_key='12345')
        db.session.add(indexer)
        db.session.commit()

        # Perform a search via a POST request
        response = self.app.post('/search', data=dict(
            query='test book'
        ))
        self.assertEqual(response.status_code, 200)

        # Check that the mock was called correctly
        mock_search.assert_called_once_with('http://test.indexer.com', '12345', 'test book')

        # Check that the fake result is in the response data
        self.assertIn(b'Fake Book Title', response.data)


class DownloadClientTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_download_client(self):
        # test adding a download client
        response = self.app.post('/add_download_client', data=dict(
            name='Test Client',
            host='localhost',
            port=8080,
            username='admin',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # check that the client was added to the database
        client = DownloadClient.query.get(1)
        self.assertIsNotNone(client)
        self.assertEqual(client.name, 'Test Client')

    @patch('app.qbittorrent.add_download')
    def test_send_to_client(self, mock_add_download):
        # Configure the mock to return a fake hash
        fake_hash = 'fake_torrent_hash_123'
        mock_add_download.return_value = fake_hash

        # Add a test book and client to the database
        book = Book(title='test book', author='Test Author')
        client = DownloadClient(name='Test Client', host='localhost', port=8080, username='admin', password='password')
        db.session.add(book)
        db.session.add(client)
        db.session.commit()

        # Perform the send to client action via a POST request
        response = self.app.post('/send_to_client', data=dict(
            link='http://fake.link/test.torrent',
            query='test book' # Pass the query that matches the book title
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the mock was called correctly
        mock_add_download.assert_called_once_with(
            host='localhost',
            port=8080,
            username='admin',
            password='password',
            link='http://fake.link/test.torrent'
        )

        # Check that the book's status and download_id were updated
        updated_book = Book.query.get(book.id)
        self.assertEqual(updated_book.status, 'downloading')
        self.assertEqual(updated_book.download_id, fake_hash)

        # Check for the success flash message
        self.assertIn(b"Download for &#39;test book&#39; successfully sent to qBittorrent!", response.data)


class JobsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.qbittorrent.get_completed_torrents')
    def test_check_completed_downloads(self, mock_get_completed):
        # Setup: Add a book that is 'downloading'
        fake_hash = 'fake_hash_for_completed_download'
        book = Book(title='Completed Book', author='Author', status='downloading', download_id=fake_hash)
        client = DownloadClient(name='Test Client', host='localhost', port=8080, username='admin', password='password')
        db.session.add(book)
        db.session.add(client)
        db.session.commit()

        # Mock: Configure the mock to return the hash of our completed book
        mock_get_completed.return_value = [fake_hash]

        # Action: Run the job function
        jobs.check_completed_downloads()

        # Assert: Check that the book's status was updated
        updated_book = Book.query.get(book.id)
        self.assertEqual(updated_book.status, 'downloaded')


if __name__ == '__main__':
    unittest.main(verbosity=2)
