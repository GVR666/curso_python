import sqlite3
import os

# Nombre del archivo de base de datos
DB_NAME = "index.db"

def get_db():
    """Establece conexión con la base de datos y permite acceder por nombre de columna."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las tablas necesarias si no existen."""
    with get_db() as conn:
        # 1. Tabla para las URLs principales a scrappear
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                status TEXT DEFAULT 'No escrapeada'
            )
        """)

        # 2. Tabla para los documentos PDF individuales encontrados
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                filename TEXT,
                url TEXT UNIQUE,
                year INTEGER,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        """)

        # 3. Tabla para los fragmentos de texto (chunks) para búsqueda difusa
        conn.execute("""
            CREATE TABLE IF NOT EXISTS text_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                chunk_text TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
        """)
        
        # Insertar la URL de la UNISON por defecto si la tabla está vacía
        try:
            conn.execute("INSERT INTO sources (url) VALUES (?)", 
                         ("https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/",))
        except sqlite3.IntegrityError:
            # Si ya existe, no hacemos nada
            pass
            
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.")