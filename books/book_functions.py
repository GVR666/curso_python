"""Book funcions.py Contains functions to work with Book objects."""

from Book import Book
from Book import load_books

def get_genres (books:list[Book])->list[str]:
    """Get all unique genres from a list of Book objects."""
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(list(genres))

def create_author_dictionary(books:list[Book])->dict[str, list[Book]]:
    """Create a dictionary where the keys are author names and the values are lists of Book objects by that author."""
    author_dict = {}
    for book in books:
        if book.author not in author_dict:
            author_dict[book.author.lower()] = []
        author_dict[book.author.lower()].append(book)
        #Multiple names or authors
        author_names = book.author.lower().split(" ")
        if len(author_names) >= 2:
            for name in author_names:
                if name not in author_dict:
                    author_dict[name] = []
                author_dict[name].append(book)
    return author_dict

if __name__ == "__main__":
    books = load_books(r"C:\Users\SAMS 8121\Documents\ProyectoCIDETH\curso_python\books\booklist2000.csv")
    genres = get_genres(books)
    author = create_author_dictionary(books)
    print(genres)
    print(author["sandra"][0])