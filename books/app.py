from flask import Flask, render_template, request
from Book import Book, load_books 
from book_functions import create_author_dictionary, create_book_dictionary, create_title_dictionary

app = Flask(__name__)

# Configuración inicial de datos
filename = 'booklist2000.csv'
books = load_books(filename)

# Diccionarios para búsquedas rápidas
author_dict = create_author_dictionary(books)
book_dict = create_book_dictionary(books)
title_dict = create_title_dictionary(books)

@app.route('/')
def index():
    return render_template('new_index.html')

@app.route('/search_by_author', methods=['GET', 'POST'])
def search_by_author():
    if request.method == 'POST':
        author = request.form['author']
        # Buscamos en el diccionario de autores (todo en minúsculas)
        books_list = author_dict.get(author.lower(), [])
        return render_template('search_by_author.html', books_list=books_list)
    else:
        # Muestra los primeros 10 libros al entrar por primera vez
        return render_template('search_by_author.html', books_list=books[:10])

@app.route('/search_by_title', methods=['GET', 'POST'])
def search_by_title():
    if request.method == 'POST':
        query = request.form['title'].lower().strip()
        # Buscamos libros donde el query esté CONTENIDO en el título
        books_list = [b for b in books if query in b.title.lower()]
        return render_template('search_by_title.html', books_list=books_list)
    else:
        return render_template('search_by_title.html', books_list=books[:10])

@app.route('/book/<book_id>')
def book_detail(book_id):
    book = book_dict.get(book_id)
    return render_template('card.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)