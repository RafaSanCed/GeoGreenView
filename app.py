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
# Actualmente, si el usuario solicita el mismo mosaico varias veces, la app lo descarga
# Esto podría ser ineficiente a largo plazo, así que intentaremos implementar una caché para
# almacenar y reutilizar los mosaicos de las coordenadas ya utilizadas

def download_google_tile(x, y, z, filename):

    # Verificamos si el archivo ya existe en caché

    if os.path.exists(filename):

        print(f"Tile {filename} encontrado en caché.")

        return
    
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
"""
Esta función utiliza rangos HSV establecidos previamente para los colores verdes. Como se ha visto en pruebas
esto puede estar ocasionando que se obtengan resultados no tan precisos en distintos mosaicos que si contienen
vegetación. Proponemos ajustar estos rangos de manera dinámica. 
"""

def calcular_porcentaje_vegetacion(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calcula el histograma del canal de saturación (hue o H)
    hue_hist = cv2.calcHist([hsv_image], [0], None, [155], [0, 155])

    # Encontramos el pico en el histograma que corresponde a los valores de verde
    green_hue_range = (80, 155)
    green_hist_peak = np.argmax(hue_hist[green_hue_range[0]:green_hue_range[1]]) + green_hue_range[0]

    # Ajustamos los rangos de forma dinámica basados en el pico detectado
    hue_min = max(green_hist_peak - 10, 0)
    hue_max = min(green_hist_peak + 10, 140)

    # Se calcula la mediana para la saturación (S) y el valor (V) para reducir la sensibilidad al ruido
    sat_median = np.median(hsv_image[:, :, 1])
    val_median = np.median(hsv_image[:, :, 2])

    # Ajustamos los rangos alrededor de la mediana, con algunos márgenes
    saturation_min = max(sat_median - 25, 0)
    saturation_max = min(sat_median + 25, 255)
    value_min = max(val_median - 25, 0)
    value_max = min(val_median + 25, 255)

    # Creamos la máscara para la vegetación basados en los rangos HSV ajustados
    mask = cv2.inRange(hsv_image, 
                       np.array([hue_min, saturation_min, value_min], np.uint8), 
                       np.array([hue_max, saturation_max, value_max], np.uint8))

    # Calculamos el porcentaje de vegetación
    total_pixels = image.shape[0] * image.shape[1]
    vegetation_pixels = np.sum(mask > 0)
    porcentaje_vegetacion = (vegetation_pixels / total_pixels) * 100

    green_lower = np.array([54, 30, 0])
    green_upper = np.array([170, 255, 255])
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, green_lower, green_upper)
    green_extract = cv2.bitwise_and(image, image, mask=mask)
    total_pixels = image.shape[0] * image.shape[1] 
    green_pixels = cv2.countNonZero(mask)  
    green_percentage = (green_pixels / total_pixels) * 100 


    return green_percentage

# Endpoint para procesar los tiles de las cuadrículas
@app.route('/process_tile', methods=['POST'])
def process_tile():
    try:
        data = request.json
        lat = data['lat']
        lng = data['lng']
        zoom = 15#data['zoom']

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
    app.run(port=5000, debug = True)
