import networkx as nx
from time import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''#Leer archivo 'nodos'
file = open ('Entregables/nodos.txt','r')
nodes = file.readline()
print("cantidad de nodos:", nodes)
file.close()'''

#Crea un grafo vacio y le asigna nodos
G = nx.DiGraph()

#Agregar arcos desde archivo txt
G=nx.read_edgelist("Entregables/arcos.txt",nodetype=int, data=(('weight',int),),create_using=nx.DiGraph())

'''
#Visualizar la red
plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
'''

#Utilizando algoritmo Dijkstra Original
def Dijkstra(G,s):
    n=G.number_of_nodes()
    predecesor = [None for i in range(n)]
    distancias=[float("inf") for i in range(n)] #lista con distancias del nodo salida al resto 
    revisados = [False for i in range(n)] #Lista Boleana: Etiqueta los nodos ya marcados
    
    for i in G.nodes():
        if i in list(G.successors(s)):
            distancias[i-1] = G.edges[s,i]['weight']
            predecesor[i-1] = s
        else:
            distancias[i-1] = float('inf')
            predecesor[i-1] = 0
            
    distancias[s-1] = 0
    revisados[s-1] = True
    predecesor[s-1] = s

    while False in revisados:
        dis_min=min(distancias)
        all_ind = [i for i,x in enumerate(revisados) if x==dis_min]
        for i in all_ind:
            if revisados[i]==False:
                revisados[i] = True
                for nodo in G.neighbors(i+1):
                    if distancias[nodo-1]>distancias[i] + G.edges[i+1,nodo]['weight']:
                        distancias[nodo-1] = distancias[i] + G.edges[i+1,nodo]['weight']
                        predecesor[nodo-1] = i+1 

    df=pd.DataFrame(data={'nodo':list(range(1,n+1)), 'predecesor':predecesor, 'distancia': distancias})
    df=df.replace(float('inf'),-1)
    return df 


#Utilizando implementación Dial del algoritmo Dijkstra
def Dial_Dijkstra(G,s):
    n=G.number_of_nodes()
    predecesor = ['' for i in range(n)]
    distancias=[float('inf') for i in range(n)]
    distancias[s-1]=0
    predecesor[s-1]=s
    
    costo_max = max([i[2]['weight'] for i in list(G.edges(data=True))])
    bucket_list = ['' for i in range(costo_max*n)]
    bucket_list[0]=s
    etiq=0
    while len(np.unique(bucket_list))>1:
        nodo=bucket_list[etiq]
        if nodo != '':
            bucket_list[etiq]=''
            for i in list(G.successors(nodo)):
                peso=etiq+G.edges[nodo,i]['weight']
                if distancias[i-1]>peso:
                    bucket_list[peso]=i
                    distancias[i-1]=peso
                    predecesor[i-1]=nodo
            etiq=0
        else:
            etiq=etiq+1
            
    df=pd.DataFrame(data={'nodo':list(range(1,n+1)), 'predecesor':predecesor, 'distancia': distancias})
    df=df.replace(float('inf'),-1)
    df=df.replace('',0)
    df = df.astype(int)
    return df


#Se le pide ingresar al usuario el nodo fuente para calcular ruta minima
s = int(input("Introduzca nodo fuente:") )

#Obtener tiempo de ejecucion de cada algoritmo
start_time= time()
df1 = Dijkstra(G,s) 
final_time= time()
ejecution_time_1 = final_time - start_time 

start_time= time()
df2 = Dial_Dijkstra(G,s)
final_time= time()
ejecution_time_2 = final_time - start_time


#Generar salida con algoritmo que posee menor tiempo de ejecucion
file = open('salida.txt','w')
file.write(str(s))
if ejecution_time_1 < ejecution_time_2:
    print("Solucion entregada con algoritmo Dijkstra")
    print("Tiempo de ejecucion final:",ejecution_time_1)
    print("Tiempo de ejecucion final de algoritmo de Dial:",ejecution_time_2)
    np.savetxt(r'salida.txt', df1.values, fmt='%d',header=str(s),comments='')
else:
    print("Solucion entregada con implementación Dial del algoritmo Dijkstra")
    print("Tiempo de ejecucion final:",ejecution_time_2)
    print("Tiempo de ejecucion final de algoritmo Dijkstra:",ejecution_time_1)
    np.savetxt(r'salida.txt', df2.values, fmt='%d',header=str(s),comments='')