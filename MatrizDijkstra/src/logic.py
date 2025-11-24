from typing import List, Tuple

INFINITY = float('inf')

def dijkstra(matriz: List[List[float]], nodoinicio: int, nododestino: int) -> Tuple[List[int], float]:
    n = len(matriz)  #número de nodos en el grafo
    dist = [INFINITY] * n 
    prev = [-1] * n
    visitado = [False] * n
    dist[nodoinicio] = 0.0 #distancia al nodo inicial

    #Buscamos el nodo u con menor distancia no visitado
    for _ in range(n):
        u = -1
        u_dist = INFINITY
        for i in range(n):
            if not visitado[i] and dist[i] < u_dist:
                u = i
                u_dist = dist[i]
        if u == -1 or u == nododestino:
            break
        visitado[u] = True
        for v in range(n):
            w = matriz[u][v]
            if w == INFINITY:
                continue
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u

    if dist[nododestino] == INFINITY:
        return [], INFINITY

    path = []
    cur = nododestino  #nodo actual
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[nododestino]