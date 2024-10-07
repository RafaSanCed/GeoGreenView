<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>GeoGreenView</h1>

  <strong>GeoGreenView</strong> es una herramienta web interactiva desarrollada para analizar y visualizar áreas verdes en zonas geográficas específicas utilizando imágenes satelitales de Google Maps. El sistema permite dividir el mapa en cuadrículas, descargar imágenes satelitales correspondientes a cada cuadrícula y aplicar un algoritmo para detectar y calcular el porcentaje de vegetación presente en cada área.

<h2>Funcionalidades</h2>
<ul>
  <li><strong>Mapa interactivo:</strong> Utiliza Leaflet.js para mostrar un mapa satelital de Google Maps.</li>
  <li><strong>Cuadrículas personalizadas:</strong> El usuario puede dibujar cuadrículas sobre la zona que desea analizar.</li>
  <li><strong>Análisis de vegetación:</strong> El sistema analiza las cuadrículas descargando imágenes satelitales de Google Maps y determina el porcentaje de zonas verdes.</li>
  <li><strong>Colores de clasificación:</strong>
<ul>
  <li><strong>Rojo:</strong> Baja vegetación (0-10% de área verde).</li>
  <li><strong>Naranja:</strong> Vegetación medio-baja (10-20% de área verde).</li>
  <li><strong>Amarillo:</strong> Vegetación moderada (20-30% de área verde).</li>
  <li><strong>Amarillo-verde:</strong> Vegetación medio-alta (30-50% de área verde).</li>
  <li><strong>Verde:</strong> Alta vegetación (50-100% de área verde).</li>
</ul>

  </li>
</ul>

<h2>Tecnologías utilizadas</h2>
<ul>
  <li><strong>Backend:</strong>
    <ul>
      <li><strong>Flask:</strong> Framework de Python utilizado para manejar las peticiones del frontend y realizar el procesamiento de imágenes.</li>
      <li><strong>OpenCV:</strong> Utilizado para procesar las imágenes descargadas, aplicar filtros y realizar el análisis de vegetación.</li>
      <li><strong>NumPy:</strong> Biblioteca de Python para operaciones matemáticas y manipulación de matrices de datos (imágenes).</li>
    </ul>
  </li>
  <li><strong>Frontend:</strong>
    <ul>
      <li><strong>Leaflet.js:</strong> Biblioteca de JavaScript para manejar los mapas interactivos y las cuadrículas.</li>
      <li><strong>HTML/CSS/JavaScript:</strong> Interfaz de usuario básica para interactuar con el sistema.</li>
    </ul>
  </li>
</ul>

<h2>Instalación</h2>

<p>Sigue estos pasos para instalar y ejecutar el proyecto en tu entorno local:</p>

<h3>Prerrequisitos</h3>
<ul>
  <li><strong>Python 3.x</strong></li>
  <li><strong>Git</strong> (opcional para clonar el repositorio)</li>
</ul>

<h3>Pasos de instalación</h3>
<ol>
  <li><strong>Clona el repositorio:</strong>
    <pre><code>git clone https://github.com/RafaSanCed/GeoGreenView.git
cd GeoGreenView</code></pre>
  </li>
  <li><strong>Crea un entorno virtual:</strong>
    <pre><code>python -m venv venv</code></pre>
  </li>
  <li><strong>Activa el entorno virtual:</strong>
    <ul>
      <li>En Windows:
        <pre><code>venv\Scripts\activate</code></pre>
      </li>
      <li>En macOS/Linux:
        <pre><code>source venv/bin/activate</code></pre>
      </li>
    </ul>
  </li>
  <li><strong>Instala las dependencias:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Configura la API de Google Maps:</strong>
    <p>Para utilizar imágenes satelitales de Google Maps, necesitarás una API Key. Agrega tu API key en el archivo <code>app.py</code> (o en cualquier archivo relevante donde se utilice la API de Google Maps) donde se solicite.</p>
  </li>
  <li><strong>Inicia el servidor:</strong>
    <pre><code>flask run</code></pre>
  </li>
  <li><strong>Accede a la aplicación:</strong>
    <p>Abre tu navegador y ve a <code>http://127.0.0.1:5000</code> para ver el mapa interactivo y comenzar a realizar el análisis de vegetación.</p>
  </li>
</ol>

<h2>Uso</h2>

<h3>Análisis de cuadrículas</h3>
<ol>
  <li><strong>Seleccionar una región:</strong> Desplázate y haz zoom en el mapa para seleccionar la región que deseas analizar.</li>
  <li><strong>Dibujar cuadrículas:</strong> Haz clic en el botón "Analizar Cuadrículas" para dibujar las cuadrículas sobre el área visible.</li>
  <li><strong>Analizar vegetación:</strong> El sistema descargará las imágenes de Google Maps, analizará cada cuadrícula, y coloreará cada una según el porcentaje de vegetación.
    <ul>
      <li><strong>Verde:</strong> Cuadrículas con más del 50% de áreas verdes.</li>
      <li><strong>Amarillo:</strong> Cuadrículas con vegetación moderada (20-50%).</li>
      <li><strong>Rojo:</strong> Cuadrículas con menos del 20% de vegetación.</li>
    </ul>
  </li>
</ol>

<h3>Gestión de imágenes</h3>
<p>Las imágenes descargadas para el análisis se almacenan temporalmente en una carpeta llamada <code>images/</code>. Cada vez que presiones el botón "Analizar Cuadrículas", las imágenes antiguas se eliminan automáticamente para asegurar que el análisis sea siempre actualizado.</p>

<h2>Estructura del proyecto</h2>
<pre><code>GeoGreenView/
│
├── app.py              # Código principal de Flask
├── static/             
│   └── css/
       └── styles.css      # Archivos CSS del frontend
├── templates/
│   └── index.html      # Página principal con el mapa interactivo
├── images/             # Carpeta para almacenar las imágenes descargadas
├── docs/               
│   └── presentation.pptx  # Archivo de presentación
├── .gitignore          
├── requirements.txt    
└── README.md           
</code></pre>

## Presentación del Proyecto

Para entender mejor el funcionamiento, las características y el impacto de **GeoGreenView**, hemos incluido una presentación de PowerPoint que explica detalladamente cómo funciona el sistema, su arquitectura, y sus beneficios. Esta presentación es ideal para mostrarla en reuniones o eventos de divulgación.

### Cómo acceder a la presentación:

La presentación se encuentra en la carpeta `docs/` con el nombre `GeoGreenView.pptx`. Puedes descargarla directamente desde el repositorio y abrirla con cualquier visor de PowerPoint.

<h2>Contribuciones</h2>
<p>Este proyecto está abierto a contribuciones. Si deseas agregar nuevas funcionalidades, mejorar el código o arreglar errores, siéntete libre de hacer un <code>fork</code> del repositorio y enviar un Pull Request.</p>

<h2>Licencia</h2>
<p>Este proyecto está bajo la licencia MIT. Consulta el archivo <code>LICENSE</code> para más detalles.</p>

</body>
</html>
