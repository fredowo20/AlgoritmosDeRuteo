import psycopg2

# Conexión a la base de datos PostgreSQL
conexion = psycopg2.connect(
    dbname="Tarea2-Ruteo",
    user="postgres",
    password="uwu",
    host="localhost"
)

cursor = conexion.cursor()

# Obtener las probabilidades de falla actualizadas
cursor.execute("SELECT index, probabilidad_falla FROM red_infraestructura")
enlaces_actualizados = cursor.fetchall()

# Preparar el contenido del archivo SQL
contenido_sql = ""
for enlace in enlaces_actualizados:
    index, probabilidad_falla = enlace
    comando_sql = f"UPDATE red_infraestructura SET probabilidad_falla = {probabilidad_falla} WHERE index = {index};\n"
    contenido_sql += comando_sql

# Escribir en un archivo
with open("./backup.sql", "w") as archivo_sql:
    archivo_sql.write(contenido_sql)

cursor.close()
conexion.close()

print("Archivo backup.sql generado exitosamente.")
