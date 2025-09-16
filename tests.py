import unittest
from unittest.mock import patch
from app import app, db
from app.models import Book, Indexer

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
