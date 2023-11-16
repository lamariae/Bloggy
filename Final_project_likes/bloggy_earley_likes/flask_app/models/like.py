from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bloggy import Bloggy

class Like:
    db = "bloggy_schema_likes"

    def __init__(self, data):
        self.like_id = data['like_id']
        self.user_id = data['user_id']
        self.bloggy_id = data['bloggy_id']
        self.like_date = data['like_date']
        self.user = User.get_by_id({'id': data['user_id']})
        self.bloggy = Bloggy.get_bloggy_by_id(data['bloggy_id'])
        
    @classmethod
    def save_like(cls, data):
        query = "INSERT INTO likes (user_id, bloggy_id, like_date) VALUES (%(user_id)s, %(bloggy_id)s, NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND bloggy_id = %(bloggy_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_likes_for_bloggy(cls, bloggy_id):
        query = "SELECT * FROM likes WHERE bloggy_id = %(bloggy_id)s;"
        data = {'bloggy_id': bloggy_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        likes = [cls(row) for row in results]
        return likes
    
    
    @classmethod
    def get_like_by_user_and_bloggy(cls, user_id, bloggy_id):
        query = "SELECT * FROM likes WHERE user_id = %(user_id)s AND bloggy_id = %(bloggy_id)s;"
        data = {'user_id': user_id, 'bloggy_id': bloggy_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_liked_bloggys_for_user(cls,user_id):
        query = "SELECT bloggy_id FROM likes WHERE user_id = %(user_id)s"
        data = { 'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        liked_bloggies = [result['bloggy_id'] for result in results]
        return liked_bloggies
    
    @classmethod
    def get_total_likes_for_user(cls, user_id):
        query = "SELECT COUNT(*) AS total_likes FROM likes WHERE user_id = %(user_id)s;"
        data = {'user_id' : user_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['total_likes'] if result else 0 