from db.Connection import get_connection

class Author:
    def __init__(self,name= None, id = None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES(?)',( self.name,))
        conn.commit()
        self.id = cursor.lastrow.id
        conn.close()

    @staticmethod
    def get_id( author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM authors WHERE id = ?', (author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(id=row['id'],name=row['name']) if row else None
    
    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?""", (self.id))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def topics (self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT m.category FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        WHERE a.author_id = ?
        """, (self.id,))
        categories =[row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    

    

    
    

    
    
        




   




