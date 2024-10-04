from flask import Flask, request, jsonify, render_template
import os
import cv2
import numpy as np
import math
import requests
import shutil

app = Flask(__name__)

# Ruta donde se guardarán las imágenes
IMAGES_FOLDER = 'tiles/'

# Crear el directorio si no existe
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

# Función para convertir latitud y longitud a coordenadas de tile
def latlng_to_tile(lat, lng, zoom):
    x = int((lng + 180) / 360 * (2**zoom))
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (2**zoom))
    return x, y

# Función para descargar el mosaico (tile) desde Google Maps
def download_google_tile(x, y, z, filename):
    url = f"https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Error al descargar el tile. Código de estado: {response.status_code}")

# Función para eliminar todas las imágenes de la carpeta
def limpiar_carpeta_imagenes():
    if os.path.exists(IMAGES_FOLDER):
        shutil.rmtree(IMAGES_FOLDER)
    os.makedirs(IMAGES_FOLDER)

# Función para calcular el porcentaje de vegetación en la imagen
def calcular_porcentaje_vegetacion(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Rango de colores verdes en el espacio HSV
    rango_verde_claro = np.array([35, 50, 80], np.uint8)
    rango_verde_claro_oscuro = np.array([85, 255, 255], np.uint8)
    rango_verde_oscuro = np.array([0, 0, 0], np.uint8)
    rango_verde_oscuro_alto = np.array([85, 255, 80], np.uint8)

    # Máscaras de color verde
    mascara_verde_claro = cv2.inRange(hsv_image, rango_verde_claro, rango_verde_claro_oscuro)
    mascara_verde_oscuro = cv2.inRange(hsv_image, rango_verde_oscuro, rango_verde_oscuro_alto)

    # Combinar las máscaras
    mascara_vegetacion = cv2.bitwise_or(mascara_verde_claro, mascara_verde_oscuro)

    # Calcular el porcentaje de vegetación
    total_pixels = image.shape[0] * image.shape[1]
    vegetacion_pixels = np.sum(mascara_vegetacion > 0)
    porcentaje_vegetacion = (vegetacion_pixels / total_pixels) * 100

    return porcentaje_vegetacion

# Endpoint para procesar los tiles de las cuadrículas
@app.route('/process_tile', methods=['POST'])
def process_tile():
    try:
        data = request.json
        lat = data['lat']
        lng = data['lng']
        zoom = data['zoom']

        # Convertir a coordenadas de tile
        x, y = latlng_to_tile(lat, lng, zoom)

        # Descargar el tile y guardarlo en la carpeta
        tile_path = os.path.join(IMAGES_FOLDER, f"tile_{x}_{y}.png")
        download_google_tile(x, y, zoom, tile_path)

        # Calcular el porcentaje de vegetación
        porcentaje_vegetacion = calcular_porcentaje_vegetacion(tile_path)

        return jsonify({'porcentaje_vegetacion': porcentaje_vegetacion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para iniciar el análisis (limpia la carpeta antes de empezar)
@app.route('/start_analysis', methods=['POST'])
def start_analysis():
    try:
        # Limpiar las imágenes antes de realizar el análisis
        limpiar_carpeta_imagenes()
        return jsonify({'message': 'Carpeta limpiada con éxito, lista para nuevo análisis'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
