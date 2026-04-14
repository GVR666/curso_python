""" book_functions.py
    Contains functions to work with Book objects
"""

from Book import Book
from Book import load_books

def get_genres(books:list[Book])->list[str]:
    """Get all unique genres from a list of Book objects"""
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(list(genres))

def create_author_dictionary(books:list[Book])->dict[str,list[Book]]:
    """Create a dictionary of authors and their books"""
    author_dict = {}
    for book in books:
        if book.author.lower() not in author_dict:
            author_dict[book.author.lower()] = []
        author_dict[book.author.lower()].append(book)
        # Multiple names or authors
        author_names = book.author.lower().split(" ")
        if len(author_names) >= 2:
            for name in author_names:   
                if name not in author_dict:
                    author_dict[name] = []
                author_dict[name].append(book)
    return author_dict
def create_title_dictionary(books: list[Book]) -> dict[str, list[Book]]:
    """Crea un diccionario de palabras clave de títulos y sus libros"""
    title_dict = {}
    for book in books:
        # Pasamos a minúsculas y dividimos el título en palabras
        words = book.title.lower().split(" ")
        
        # También guardamos el título completo por si buscan exacto
        full_title = book.title.lower()
        if full_title not in title_dict:
            title_dict[full_title] = []
        title_dict[full_title].append(book)

        # Guardamos cada palabra individualmente
        for word in words:
            # Limpiamos un poco la palabra (quitar comas o puntos si quieres)
            clean_word = word.strip(".,()!?:")
            if clean_word not in title_dict:
                title_dict[clean_word] = []
            
            # Evitamos duplicados si la palabra ya agregó el libro
            if book not in title_dict[clean_word]:
                title_dict[clean_word].append(book)
                
    return title_dict

def create_book_dictionary(book_list:list)->dict[str,Book]:
    """Create a dictionary of books and their ids"""
    book_dict = {}
    for book in book_list:
        book_dict[book.id] = book
    return book_dict

if __name__ == "__main__":
    books = load_books("booklist2000.csv")
    print(get_genres(books))
    author_dict = create_author_dictionary(books)
    print(author_dict["sandra"][0])