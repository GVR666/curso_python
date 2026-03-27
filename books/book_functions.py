

from Book import Book
from Book import load_books

def get_genres(books:list[Book])->list[str]:
    genres = set()
    for book in books:
        genres.add(book.genre)
    return sorted(list(genres))

def create_author_dictionary(books:list[Book])->dict[str,list[Book]]:
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

def create_book_dictionary(book_list:list)->dict[str,Book]:
    book_dict = {}
    for book in book_list:
        book_dict[book.id] = book
    return book_dict

if __name__ == "__main__":
    books = load_books("booklist2000.csv")
    print(get_genres(books))
    author_dict = create_author_dictionary(books)
    print(author_dict["sandra"][0])