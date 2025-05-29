from db.Connection import get_connection

class Article:
    def __init__(self,id = None, title = None, author_id = None, magazine_id = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row) if row else None
    
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                       (self.title, self.author_id, self.magazine_id))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()