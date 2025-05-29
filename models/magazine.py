from db.Connection import get_connection

class Magazine:
    def __init__(self, id = None, name = None, category = None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.exucute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT a.*, COUNT(*) as article_count
        FROM authors a
        JOIN articles art ON a.id = art.author_id
        WHERE art.magazine_id = ?
        GROUP BY a.id
        HAVING article_count > 2
        """, (self.id,))
        results = cursor.fetchall()
        conn.close()
        return results

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT DISTINCT a.* FROM authors a
        JOIN articles art ON art.author_id = a.id
        WHERE art.magazine_id = ?
        """, (self.id,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def article_title(self):
        conn = get_connection()
        cursor = conn.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles