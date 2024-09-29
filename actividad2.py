import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Definir la base de conocimiento con reglas lógicas
base_conocimiento = {
    "conectado": {
        ("Caña brava", "Homecenter"): 10,
        ("Homecenter", "Guacamaya"): 15,
        ("Homecenter", "Batallon"): 15,
        ("Batallon", "Cementerio central"): 15,
        ("Guacamaya", "Cruz roja"): 20,
        ("Cruz roja", "Universidad Surcolombiana"): 25,
        ("Universidad Surcolombiana", "Cementerio central"): 35,
        ("Universidad Surcolombiana", "Centro"): 10,
        ("Cementerio central", "Centro"): 20,
    }
}

# Crear el grafo
grafo = nx.Graph()

# Agregar las conexiones al grafo
for conexion, distancia in base_conocimiento["conectado"].items():
    estacion1, estacion2 = conexion
    grafo.add_edge(estacion1, estacion2, weight=distancia)

# Función para encontrar la mejor ruta
def encontrar_mejor_ruta(origen, destino, visitados=None, ruta_actual=None, distancia_actual=0):
    if visitados is None:
        visitados = []
    if ruta_actual is None:
        ruta_actual = []

    # Agregar la estación actual a la ruta y marcarla como visitada
    ruta_actual.append(origen)
    visitados.append(origen)

    # Verificar si se ha llegado al destino
    if origen == destino:
        # Imprimir la ruta y la distancia total
        print("Ruta encontrada:", ruta_actual)
        print("Distancia total:", distancia_actual)
        return ruta_actual

    # Obtener todas las conexiones de la estación actual
    conexiones = base_conocimiento["conectado"].keys()

    # Iniciar la mejor ruta y distancia con nulas
    mejor_ruta = None
    mejor_distancia = float("inf")

    # Recorrer todas las conexiones de la estación actual
    for conexion in conexiones:
        if origen == conexion[0] and conexion[1] not in visitados:
            # Calcular la distancia acumulada para esta conexión
            distancia = distancia_actual + base_conocimiento["conectado"][conexion]

            # Realizar una llamada recursiva para encontrar la mejor ruta desde la conexión actual
            nueva_ruta = encontrar_mejor_ruta(
                conexion[1], destino, visitados.copy(), ruta_actual.copy(), distancia
            )

            # Actualizar la mejor ruta y distancia si se ha encontrado una ruta más corta
            if nueva_ruta and distancia < mejor_distancia:
                mejor_ruta = nueva_ruta
                mejor_distancia = distancia

    return mejor_ruta

# Encontrar la mejor ruta
ruta = encontrar_mejor_ruta("Caña brava", "Centro")

# Generar datos para la gráfica en forma de campana
mu, sigma = 0, 0.1  # media y desviación estándar
datos = np.random.normal(mu, sigma, 1000)

# Visualizar la gráfica en forma de campana
plt.figure(figsize=(12, 6))

# Gráfica de la distribución normal
plt.subplot(1, 2, 1)
plt.hist(datos, bins=30, density=True, alpha=0.5, color='blue')
plt.xlabel("Valores")
plt.ylabel("Densidad")
plt.title("Gráfica en forma de campana")
plt.grid(True)

# Visualizar el grafo y la ruta encontrada
plt.subplot(1, 2, 2)
pos = nx.spring_layout(grafo)
nx.draw(grafo, pos, with_labels=True, node_size=500, font_size=10)
etiquetas = nx.get_edge_attributes(grafo, "weight")
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=etiquetas)
ruta_aristas = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
nx.draw_networkx_edges(grafo, pos, edgelist=ruta_aristas, edge_color="red", width=2)

plt.title("Grafo y Ruta Encontrada")
plt.show()