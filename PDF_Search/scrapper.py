import os
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from markitdown import MarkItDown
import pytesseract
from pdf2image import convert_from_path
from database import get_db
from urllib.parse import urljoin  # Correcto para Python 3

# --- CONFIGURACIÓN DE RUTAS ---
# Estas rutas permiten que Python encuentre los programas externos
PATH_POPPLER = r'C:\Users\SAMS 8121\Documents\Poppler\poppler-26.02.0\Library\bin' 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

DOWNLOAD_PATH = "downloaded_pdfs"
MARKDOWN_PATH = "markdown_files"

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
os.makedirs(MARKDOWN_PATH, exist_ok=True)

def extract_year_from_text(text, filename):
    """ Intenta deducir el año del documento """
    match = re.search(r'\b(202[0-9]|19[0-9]{2})\b', text)
    if match:
        return int(match.group(1))
    match_file = re.search(r'\b(202[0-9])\b', filename)
    return int(match_file.group(1)) if match_file else 2026

def run_ocr(pdf_path):
    """ Convierte PDF a imágenes y aplica OCR en inglés para evitar errores de librería """
    print(f"[OCR] Procesando escaneo para: {pdf_path}")
    try:
        # Se usa PATH_POPPLER para renderizar las páginas
        pages = convert_from_path(pdf_path, 300, poppler_path=PATH_POPPLER)
        
        full_text = ""
        for i, page in enumerate(pages):
            # Cambiado a 'eng' para evitar el error de "spa.traineddata"
            text = pytesseract.image_to_string(page, lang='eng')
            full_text += f"\n--- Página {i+1} ---\n" + text
        return full_text
    except Exception as e:
        print(f"[OCR Error] No se pudo procesar el archivo: {e}")
        return ""

def process_source_url(source_id):
    conn = get_db()
    source = conn.execute("SELECT url FROM sources WHERE id = ?", (source_id,)).fetchone()
    if not source:
        return
    
    url = source['url']
    print(f"--- Iniciando escrapeo de: {url} ---")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Error accediendo a {url}: {e}")
        return

    soup = BeautifulSoup(res.text, 'html.parser')
    converter = MarkItDown()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            if not href.startswith('http'):
                href = urljoin(url, href)

            filename = href.split('/')[-1]
            pdf_file_path = os.path.join(DOWNLOAD_PATH, filename)
            md_file_path = os.path.join(MARKDOWN_PATH, f"{os.path.splitext(filename)[0]}.md")

            # Descarga del PDF
            print(f"Descargando: {filename}...")
            try:
                pdf_res = requests.get(href, timeout=10)
                with open(pdf_file_path, 'wb') as f:
                    f.write(pdf_res.content)
            except Exception as e:
                print(f"Error descargando {filename}: {e}")
                continue

            # Intento de conversión directa a texto
            content = ""
            try:
                result = converter.convert(pdf_file_path)
                content = result.markdown or result.text_content
            except Exception:
                content = ""

            # Si el PDF es una imagen (poco texto), aplicamos OCR
            if not content or len(content.strip()) < 50:
                content = run_ocr(pdf_file_path)

            # Guardar el texto extraído localmente
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Extraer año e indexar en la base de datos
            year = extract_year_from_text(content, filename)
            
            try:
                cursor = conn.execute(
                    "INSERT INTO documents (source_id, filename, url, year) VALUES (?, ?, ?, ?)",
                    (source_id, filename, href, year)
                )
                doc_id = cursor.lastrowid

                # Fragmentar en trozos para el buscador de Levenshtein
                chunk_size = 150
                chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size) if content[i:i+chunk_size].strip()]
                
                for chunk in chunks:
                    conn.execute("INSERT INTO text_chunks (document_id, chunk_text) VALUES (?, ?)", (doc_id, chunk))
            except sqlite3.IntegrityError:
                pass

    conn.execute("UPDATE sources SET status = 'Escrapeada' WHERE id = ?", (source_id,))
    conn.commit()
    conn.close()
    print(f"--- Proceso finalizado con éxito ---")