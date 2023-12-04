# Algoritmos De Ruteo y Redes Resilientes

1. Debe descargar la infraestructura chilena reportada en el Estudio y Recomendaciones sobre la Resiliencia de la infraestructura de la Internet chilena.
2. Crear una tabla que permita cargar la información descargada previamente y que permita asignar una probabilidad de falla a cada enlace (por defecto cada enlace tiene probabilidad cero de fallar).
3. Convertir la infraestructura a una topología de red utilizando pgr_createTopology.
4. Hacer un script que permita calcular el ATTR de la infraestructura en operación.
5. Dado que recientemente fue la conferencia de seguridad 8.8, deberá buscar la información del sismo 8.8 en su formato geojson en https://earthquake.usgs.gov/earthquakes/search/Links to an external site.
6. Indicar un modelo de falla a partir del epicentro del terremoto (buscar un modelo en la literatura).
7. Hacer un script o sql que permita calcular las nuevas probabilidades de falla de cada enlace.
8. Generar un .sql con las nuevas probabilidades de falla llamado backup.sql
9. Indicar el nuevo ATTR de la infraestructura crítica, producto del terremoto 8.8
10. Indicar 5 reflexiones sobre los resultados obtenidos de conectividad con respecto a la magnitud de las fallas reportadas el 27F.
