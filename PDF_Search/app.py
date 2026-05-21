from flask import Flask, render_template, request, redirect, url_for, jsonify
import Levenshtein
from database import get_db
from scrapper import process_source_url

app = Flask(__name__)

@app.route('/')
def home():
    conn = get_db()
    total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    
    # Sumar palabras aproximadas por chunk
    chunks = conn.execute("SELECT chunk_text FROM text_chunks").fetchall()
    total_words = sum(len(chunk['chunk_text'].split()) for chunk in chunks)
    
    # Agrupación por año
    years_data = conn.execute("SELECT year, COUNT(*) as c FROM documents GROUP BY year ORDER BY year DESC").fetchall()
    conn.close()
    return render_template('home.html', total_docs=total_docs, total_words=total_words, years_data=years_data)

@app.route('/scrapper')
def scrapper():
    conn = get_db()
    sources = conn.execute("SELECT * FROM sources").fetchall()
    data = []
    for src in sources:
        docs = conn.execute("SELECT filename FROM documents WHERE source_id = ?", (src['id'],)).fetchall()
        data.append({
            'id': src['id'],
            'url': src['url'],
            'status': src['status'],
            'docs': [d['filename'] for d in docs]
        })
    conn.close()
    return render_template('scrapper.html', data=data)

@app.route('/scrapper/run/<int:source_id>', methods=['POST'])
def run_scrapper(source_id):
    process_source_url(source_id)
    return redirect(url_for('scrapper'))

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    conn = get_db()
    if request.method == 'POST':
        new_url = request.form.get('url')
        if new_url:
            try:
                conn.execute("INSERT INTO sources (url) VALUES (?)", (new_url,))
                conn.commit()
            except Exception:
                pass
        return redirect(url_for('configuration'))
    
    sources = conn.execute("SELECT url FROM sources").fetchall()
    conn.close()
    return render_template('config.html', sources=sources)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    # Si viene del navbar el umbral por defecto es 0.50, si viene de la vista /search usa el slider
    threshold = float(request.args.get('threshold', 0.50))
    
    results = []
    if query:
        conn = get_db()
        # Traemos los chunks y sus datos de documento asociados
        chunks = conn.execute("""
            SELECT tc.chunk_text, d.url, d.filename 
            FROM text_chunks tc 
            JOIN documents d ON tc.document_id = d.id
        """).fetchall()
        
        query_lower = query.lower()
        for row in chunks:
            text_lower = row['chunk_text'].lower()
            # Si el chunk contiene el término de búsqueda de manera directa o difusa
            ratio = Levenshtein.ratio(text_lower, query_lower)
            if ratio >= threshold:
                results.append({
                    'url': row['url'],
                    'filename': row['filename'],
                    'text': row['chunk_text'],
                    'percentage': round(ratio * 100, 2)
                })
        conn.close()
        # Ordenar por mayor similitud
        results = sorted(results, key=lambda x: x['percentage'], reverse=True)

    return render_template('search.html', query=query, threshold=threshold, results=results)

if __name__ == '__main__':
    app.run(debug=True)