from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import Bcrypt

class User:
    db = 'bloggy_schema_likes'
    def __init__(self, user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.email = user['email']
        self.password = user['password']
        self.profile_pic = user['profile_pic']
        self.user_bio = user['user_bio']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_total_bloggys(cls, user_id):
        query = """
            SELECT COUNT(*) as total_bloggys FROM bloggys WHERE user_id = %(user_id)s;
        """
        data = {
            'user_id' : user_id
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]['total_bloggys']
        else:
            return 0
    

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid


