from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    db = "users_books"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def create_user(cls, data):
        """Add new user to db"""
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_user(cls, data):
        """Update user info"""
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_user_by_id(cls, data):
        """Get the user by id"""
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return cls(connectToMySQL(cls.db).query_db(query, data)[0])

    @classmethod
    def get_user_by_email(cls, data):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls,data):
        """Get all users"""
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_users = []
        for u in results:
            all_users.append(cls(u))
        return all_users

    @classmethod
    def is_valid_user(cls,user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email associated with another user.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!", "register")
            is_valid = False
        if len(user["first_name"]) <= 3:
            is_valid = False
            flash("First name is required.", "register")
        if len(user["last_name"]) <= 3:
            flash("Last name is required.", "register")
            is_valid = False
        if len(user["password"]) <= 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords must match", "register")
        return is_valid

    @staticmethod
    def validate_account(user):
            is_valid = True
            if len(user['first_name']) < 3:
                flash("The first name must be at least 3 characters.", "danger")
                is_valid = False
            if len(user['last_name']) < 3:
                flash("The last name must be at least 3 characters.", "danger")
                is_valid = False
            if len(user['email']) < 3:
                flash("The email must be at least 3 characters.", "danger")
                is_valid = False
            if not EMAIL_REGEX.match(user['email']):
                flash("Email is not valid!", "danger")
                is_valid = False
                return is_valid
            return is_valid