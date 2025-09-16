import unittest
from app import app, db
from app.models import Book

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

if __name__ == '__main__':
    unittest.main(verbosity=2)
