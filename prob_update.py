import psycopg2
import math

# Conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    dbname="Tarea2-Ruteo",
    user="postgres",
    password="uwu",
    host="localhost"
)

cursor = conexion.cursor()

# Propiedades terremoto
magnitud = 8.8
profundidad = 36

# Coordenadas del epicentro del terremoto
epicentro_lat = -36.122
epicentro_lon = -72.898

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Fórmula de Haversine para calcular la distancia en km
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = R * c
    return distancia

def modelo_probabilidad_falla(distancia, magnitud, profundidad):
    # Factores de ajuste
    factor_magnitud = magnitud / 6.1
    factor_profundidad = 1 / (profundidad / 70 + 1)

    # Modelo de Atenuación Sísmica 
    atenuacion = math.exp(-distancia / 300)

    # Calcular la probabilidad de falla
    probabilidad_falla = min(1, max(0, atenuacion * factor_magnitud * factor_profundidad))
    #print(factor_magnitud, factor_profundidad, atenuacion)

    return probabilidad_falla

# Obtener el punto medio de cada enlace de la red
cursor.execute("SELECT index, ST_X(ST_Centroid(geometria)), ST_Y(ST_Centroid(geometria)) FROM red_infraestructura")
enlaces = cursor.fetchall()

for enlace in enlaces:
    index, enlace_lon, enlace_lat = enlace
    distancia = calcular_distancia(epicentro_lat, epicentro_lon, enlace_lat, enlace_lon)
    probabilidad_falla = modelo_probabilidad_falla(distancia, magnitud, profundidad)
    #print(index, enlace_lon, enlace_lat, distancia, probabilidad_falla)

    # Actualizar la probabilidad de falla en la base de datos
    cursor.execute("UPDATE red_infraestructura SET probabilidad_falla = %s WHERE index = %s", (probabilidad_falla, index))

conexion.commit()
cursor.close()
conexion.close()
