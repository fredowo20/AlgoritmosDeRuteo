import json
import psycopg2
from psycopg2.extras import execute_batch

# Conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    dbname="Tarea2-Ruteo",
    user="postgres",
    password="uwu",
    host="localhost"
)

cursor = conexion.cursor()

# Leer el archivo JSON
with open('Fibrapticadetectada.json', 'r') as file:
    data = json.load(file)

# Preparar los datos para la inserción
datos_para_insertar = []
for feature in data['features']:
    properties = feature['properties']
    geometry = feature['geometry']
    
    if geometry['type'] == 'LineString':
        line_string = "SRID=4326;LINESTRING(" + ', '.join([' '.join(map(str, coord)) for coord in geometry['coordinates']]) + ")"
        datos_para_insertar.append((
            properties.get('id'),
            properties.get('id_2'),
            properties.get('id_3'),
            properties.get('id_2_2'),
            properties.get('id_4'),
            line_string
        ))
    elif geometry['type'] == 'MultiLineString':
        for line in geometry['coordinates']:
            line_string = "SRID=4326;LINESTRING(" + ', '.join([' '.join(map(str, coord)) for coord in line]) + ")"
            datos_para_insertar.append((
                properties.get('id'), 
                properties.get('id_2'),
                properties.get('id_3'),
                properties.get('id_2_2'),
                properties.get('id_4'),
                line_string
            ))

# Inserción por lotes en la base de datos
query = """
INSERT INTO red_infraestructura (id, id_2, id_3, id_2_2, id_4, geometria)
VALUES (%s, %s, %s, %s, %s, ST_GeomFromEWKT(%s))
"""

execute_batch(cursor, query, datos_para_insertar)
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()
