import psycopg2

# Conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    dbname="Tarea2-Ruteo",
    user="postgres",
    password="uwu",
    host="localhost"
)

cursor = conexion.cursor()

# Selección de pares de nodos representativos
query_nodos = "SELECT id FROM red_infraestructura_vertices_pgr LIMIT 500;"
cursor.execute(query_nodos)
nodos = cursor.fetchall()

# Calcular la confiabilidad de los caminos entre los nodos seleccionados
confiabilidades = []
for nodo_origen in nodos:
    for nodo_destino in nodos:
        if nodo_origen != nodo_destino:
            # Encuentra el camino más corto (o varios caminos)
            query_camino = f"""
            SELECT infra.index, (1 - probabilidad_falla) as confiabilidad_enlace
            FROM pgr_dijkstra(
                'SELECT index as id, source, target, ST_Length(geometria) as cost FROM red_infraestructura',
                {nodo_origen[0]}, {nodo_destino[0]}, directed := false
            ) as rutas
            JOIN red_infraestructura as infra ON rutas.edge = infra.index;
            """
            cursor.execute(query_camino)
            confiabilidad_camino = 1
            resultados = cursor.fetchall()
            for _, confiabilidad_enlace in resultados:
                confiabilidad_camino *= confiabilidad_enlace
            confiabilidades.append(confiabilidad_camino)

# Calcular el ATTR
if confiabilidades:
    attr_promedio = sum(confiabilidades) / len(confiabilidades)
else:
    attr_promedio = 0

print(f"ATTR de la Red: {attr_promedio}")

# Cerrar la conexión
cursor.close()
conexion.close()
