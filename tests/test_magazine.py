import pytest
from db.Connection import get_connection
from models.author import Author
from models.magazine import Magazine
from models.article import Article

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
        DELETE FROM sqlite_sequence;
    """)
    conn.commit()
    conn.close()

def test_magazine_save_and_retrieve():
    magazine = Magazine(name="Science Weekly", category="Science")
    magazine.save()

    fetched = Magazine.find_by_id(magazine.id)
    assert fetched.name == "Science Weekly"
    assert fetched.category == "Science"

def test_magazine_contributors():
    magazine = Magazine(name="Nature Journal", category="Environment")
    magazine.save()

    author1 = Author(name="Alice")
    author1.save()
    author2 = Author(name="Bob")
    author2.save()

    Article(title="Climate Change", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Green Tech", author_id=author2.id, magazine_id=magazine.id).save()

    contributors = magazine.contributors()
    contributor_names = [a['name'] for a in contributors]

    assert "Alice" in contributor_names
    assert "Bob" in contributor_names