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

def test_article_save_and_retrieve():
    author = Author(name="John Doe")
    author.save()

    magazine = Magazine(name="Tech Today", category="Technology")
    magazine.save()

    article = Article(title="AI in 2025", author_id=author.id, magazine_id=magazine.id)
    article.save()

    fetched = Article.find_by_id(article.id)
    assert fetched.title == "AI in 2025"
    assert fetched.author_id == author.id
    assert fetched.magazine_id == magazine.id

def test_article_find_by_title():
    author = Author(name="Jane Smith")
    author.save()

    magazine = Magazine(name="Health Monthly", category="Health")
    magazine.save()

    article = Article(title="Nutrition Tips", author_id=author.id, magazine_id=magazine.id)
    article.save()

    results = Article.find_by_title("Nutrition Tips")
    assert len(results) == 1
    assert results[0].title == "Nutrition Tips"

