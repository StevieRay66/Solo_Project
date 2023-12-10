from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user


class Book:
    db = "users_books"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.user_ids_who_favorited = []
        self.users_who_favorited = []

    @classmethod
    def create_book(cls,data):
        """Create a book"""
        query = "INSERT INTO books (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def favorite(cls,data):
        query = "INSERT INTO favorites (user_id, book_id) VALUES (%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_books(cls):
        """Get all the books in db"""
        query = '''SELECT * FROM books
                JOIN users AS creators ON books.user_id = creators.id
                LEFT JOIN favorites ON favorites.book_id = books.id
                LEFT JOIN users AS users_who_favorited ON favorites.user_id = users_who_favorited.id;'''
        results = connectToMySQL(cls.db).query_db(query)
        all_books = []
        for r in results:
            new_book = True
            users_who_favorited_data = {
                'id': r['users_who_favorited.id'],
                'first_name': r['users_who_favorited.first_name'],
                'last_name': r['users_who_favorited.last_name'],
                'email': r['users_who_favorited.email'],
                'password': r['users_who_favorited.password'],
                'created_at': r['users_who_favorited.created_at'],
                'updated_at': r['users_who_favorited.updated_at']
            }
            num_of_book = len(all_books)
            print(num_of_book)

            if num_of_book > 0:

                last_book = all_books[num_of_book-1]
                if last_book.id == r['id']:
                    last_book.user_ids_who_favorited.append(r['users_who_favorited.id'])
                    last_book.users_who_favorited.append(user.User(users_who_favorited_data))
                    new_book = False

            if new_book:
                book = cls(r)

                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                book.creator = one_user

                if r['users_who_favorited.id']:
                    book.user_ids_who_favorited.append(r['users_who_favorited.id'])
                    book.users_who_favorited.append(user.User(users_who_favorited_data))
                    print(book.users_who_favorited)

                all_books.append(book)
        return all_books

    @classmethod
    def get_one_book(cls,data):
        """Get one book to display"""
        query = '''SELECT * FROM books
                JOIN users AS creators ON books.user_id = creators.id
                LEFT JOIN favorites ON favorites.book_id = books.id
                LEFT JOIN users AS users_who_favorited ON favorites.user_id = users_who_favorited.id WHERE books.id = %(id)s;'''

        result = connectToMySQL(cls.db).query_db(query, data)

        if len(result) < 1:
            return False

        new_book = True
        for r in result:
            if new_book:

                book = cls(result[0])
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                book.creator = one_user
                new_book = False

            if r['users_who_favorited.id']:
                users_who_favorited_data = {
                    'id': r['users_who_favorited.id'],
                    'first_name': r['users_who_favorited.first_name'],
                    'last_name': r['users_who_favorited.last_name'],
                    'email': r['users_who_favorited.email'],
                    'password': r['users_who_favorited.password'],
                    'created_at': r['users_who_favorited.created_at'],
                    'updated_at': r['users_who_favorited.updated_at']
                }
                users_who_favorited = user.User(users_who_favorited_data)
                book.users_who_favorited.append(users_who_favorited)
                book.user_ids_who_favorited.append(r['users_who_favorited.id'])
        return book


    @classmethod
    def update_book(cls,data):
        """Update the book"""
        query = "UPDATE books SET title=%(title)s, description=%(description)s, WHERE books.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def delete_book(cls,data):
        """Delete book"""
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unfavorite(cls,data):
        query = "DELETE FROM favorites WHERE user_id=%(user_id)s AND book_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @staticmethod
    def validate_form(book):
        """Validate the new book create form"""
        is_valid = True
        if len(book['title']) < 2:
            flash("The Title must be at least 2 characters.", "danger")
            is_valid = False
        if len(book['description']) < 10:
            flash("The description must be at least 10 characters.", "danger")
            is_valid = False
        return is_valid