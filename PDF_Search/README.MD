Buenas profesor esta es mi pagina "inteligente" que puede leer los links como el de la unison para bajarse los PDFS y "leerselos"
Asi es como funciona:

Scrapeo: El programa va a la web de la Uni y busca todos los botones que digan "pdf"

Magia de OCR: Como muchos PDFs son escaneos viejos, el programa usa Tesseract para reconocer las letras una por una.

Buscador con "tolerancia": Usé un algoritmo llamado Levenshtein. Esto sirve para que, si escribes algo mal (como "Unversidad"), el buscador sea buena onda y te encuentre 
los resultados de "Universidad" de todos modos.

LAS CARPETAS IMPORTANTES DEL PROGRAMA

📄 app.py: El corazón que prende la página web.

🤖 scrapper.py: El robot que descarga y lee los archivos.

📁 downloaded_pdfs: Aquí se guardan los PDFs originales.

📝 markdown_files: Aquí se guarda todo el texto que el robot logró extraer.

🗄️ index.db: La base de datos donde se guarda todo el "índice" para buscar rápido.

PASOS PARA USAR EL PROGRAMA:

Borra la base de datos vieja (si hay una) y corre python database.py.

Prende el servidor con python app.py.

Entra a http://127.0.0.1:5000 en tu navegador.

En Configuration, pega un link de la UNISON.

En Scrapper, dale al botón de iniciar y espera a que la terminal deje de sacar texto(esto durara unos minutos).

HECHO POR GUILLERMO VAZQUEZ ROJAS, ESTUDIANTE DE LA UNIVERSIDAD DE SONORA
HERMOSILLO SONORA-2026
Fecha:20/05/2026



