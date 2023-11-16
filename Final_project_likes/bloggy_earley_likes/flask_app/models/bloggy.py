from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Bloggy:
    db = "bloggy_schema_likes"
    def __init__(self, bloggy):
        self.bloggy_id = bloggy['bloggy_id']
        self.title = bloggy['title']
        self.content = bloggy['content']
        self.created_at = bloggy['created_at']
        self.updated_at = bloggy['updated_at']
        self.user_id = bloggy['user_id']
        self.user = {'first_name' : bloggy['first_name'], 'last_name': bloggy['last_name']}

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO bloggys (title, content, created_at, user_id)
            VALUES (%(title)s, %(content)s, %(created_at)s, %(user_id)s);
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def save_update(cls, data):
        query = """
        UPDATE bloggys SET title = %(title)s, content = %(content)s
        WHERE bloggy_id = %(bloggy_id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_bloggys(cls):
        query = """
            SELECT bloggys.*, users.first_name, users.last_name
            FROM bloggys
            JOIN users ON bloggys.user_id = users.id
            ORDER BY bloggys.created_at DESC;
        """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        bloggys = []
        for row in results:
            bloggys.append(cls(row))
        return bloggys

    @classmethod
    def get_bloggys_by_id(cls, user_id):
        #query = "SELECT * FROM bloggys WHERE user_id = %(user_id)s;"
        query = """
            SELECT bloggys.*, users.first_name, users.last_name
            FROM bloggys
            JOIN users ON bloggys.user_id = users.id
            WHERE bloggys.user_id = %(user_id)s
            ORDER BY bloggys.created_at DESC;
        """
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        bloggys = []
        for bloggy_data in results:
            bloggy = cls(bloggy_data)
            bloggys.append(bloggy)
        #for bloggy in bloggys:
            #print(f"Bloggy Title: {bloggy.title}, Bloggy Content: {bloggy.content}, Date Added: {bloggy.created_at}")
        return bloggys
    
    @classmethod
    def get_bloggy_by_id(cls, bloggy_id):
        #query = "SELECT * FROM bloggys WHERE bloggy_id = %(bloggy_id)s;"
        query = """
            SELECT bloggys.*, users.first_name, users.last_name
            FROM bloggys
            JOIN users ON bloggys.user_id = users.id
            WHERE bloggys.bloggy_id = %(bloggy_id)s;
        """
        data = {'bloggy_id' : bloggy_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    @classmethod
    def delete_bloggy(cls,bloggy_id):
        query = "DELETE from bloggys WHERE bloggy_id = %(bloggy_id)s;"
        data = {'bloggy_id' : bloggy_id}
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, bloggy_id, title, content):
        query = """
        UPDATE bloggys SET title = %(title)s, content = %(content)s 
        WHERE bloggy_id = %(bloggy_id)s;
        """
        data = {
            'title' : title,
            'content' : content,
            'bloggy_id' : bloggy_id
        }
        connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_create_bloggy(bloggy):
        is_valid = True
        if len(bloggy['title'])<3:
            flash("Bloggy title must be at least 3 characters", "create_bloggy")
            is_valid = False
        if len(bloggy['content']) < 3:
            flash("Bloggy must be at least 3 characters", "create_bloggy")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_edit_bloggy(bloggy):
        is_valid = True
        if len(bloggy['title']) < 3:
            flash("Bloggy title must be at least 3 characters", "edit_bloggy")
            is_valid = False
        if len(bloggy['content']) < 3:
            flash("Bloggy must be at least 3 characters", "edit_bloggy")
            is_valid = False
        
        return is_valid