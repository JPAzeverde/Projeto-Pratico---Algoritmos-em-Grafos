import os                       # Para manipulação de caminhos e arquivos
import math                    # Para funções matemáticas básicas
import heapq                   # Para a fila de prioridade do Dijkstra
import numpy as np             # Para manipular matrizes e vetores com eficiência
from collections import defaultdict, deque  # Para listas de adjacência e BFS/DFS

# analiseGrafo.py (CONTINUAÇÃO)

class Grafo:
    def __init__(self):
        self.capacidade = 0
        self.deposito = 0
        self.num_vertices = 0

        # Estruturas principais
        self.adj_arestas = defaultdict(list)   # lista de adjacência de arestas (mão dupla)
        self.adj_arcos = defaultdict(list)     # lista de adjacência de arcos (mão única)

        self.vertices_requeridos = set()
        self.arestas_requeridas = []           # (de, para, custo, demanda, servico)
        self.arcos_requeridos = []             # (de, para, custo, demanda, servico)

        self.arestas_opcionais = []
        self.arcos_opcionais = []

    def ler_arquivo(self, nome_arquivo):
        self.capacidade = 0
        self.deposito = 0
        self.num_vertices = 0

        self.adj_arestas = defaultdict(list)
        self.adj_arcos = defaultdict(list)

        self.vertices_requeridos = set()
        self.arestas_requeridas = []
        self.arcos_requeridos = []

        self.arestas_opcionais = []
        self.arcos_opcionais = []

        self.todos_servicos = []

        estado = "NONE"
        sid = 1  # ID global para serviços, na ordem de leitura

        with open(nome_arquivo, 'r') as arq:
            for linha in arq:
                linha = linha.strip()
                if not linha or linha.startswith("Name:") or linha.startswith("based on"):
                    continue

                partes = linha.split()
                if not partes:
                    continue
                palavra = partes[0]

                # Troca de estado
                if palavra == "Capacity:":
                    self.capacidade = int(partes[1])
                    continue
                elif palavra == "Depot" and partes[1] == "Node:":
                    self.deposito = int(partes[2])
                    continue
                elif palavra == "#Nodes:":
                    self.num_vertices = int(partes[1])
                    continue
                elif palavra == "ReN.":
                    estado = "REN"
                    continue
                elif palavra == "ReE.":
                    estado = "REE"
                    continue
                elif palavra == "ReA.":
                    estado = "REA"
                    continue
                elif palavra == "EDGE":
                    estado = "EDGE"
                    continue
                elif palavra == "ARC":
                    estado = "ARC"
                    continue

                try:
                    # NÓS REQUERIDOS
                    if estado == "REN" and palavra.startswith('N'):
                        v = int(palavra[1:])
                        demanda, custo = map(int, partes[1:3])
                        self.vertices_requeridos.add(v)
                        self.todos_servicos.append(('N', sid, v, v, custo, demanda))
                        sid += 1

                    # ARESTAS REQUERIDAS
                    elif estado == "REE" and palavra.startswith('E'):
                        if len(partes) < 6:
                            print(f" Linha REE inválida: {linha}")
                            continue
                        de, para, custo, demanda, _ = map(int, partes[1:6])
                        self.arestas_requeridas.append((de, para, custo, demanda, sid))
                        self.adj_arestas[de].append((para, custo))
                        self.adj_arestas[para].append((de, custo))
                        self.todos_servicos.append(('E', sid, de, para, custo, demanda))
                        sid += 1

                    # ARCOS REQUERIDOS
                    elif estado == "REA" and palavra.startswith('A'):
                        if len(partes) < 6:
                            print(f" Linha REA inválida: {linha}")
                            continue
                        de, para, custo, demanda, _ = map(int, partes[1:6])
                        self.arcos_requeridos.append((de, para, custo, demanda, sid))
                        self.adj_arcos[de].append((para, custo))
                        self.todos_servicos.append(('A', sid, de, para, custo, demanda))
                        sid += 1

                    # ARESTAS OPCIONAIS
                    elif estado == "EDGE" and palavra.startswith('E'):
                        if len(partes) < 4:
                            print(f" Linha EDGE inválida: {linha}")
                            continue
                        _, de, para, custo = partes
                        de, para, custo = int(de), int(para), int(custo)
                        self.arestas_opcionais.append((de, para, custo, 0, 0))
                        self.adj_arestas[de].append((para, custo))
                        self.adj_arestas[para].append((de, custo))

                    # ARCOS OPCIONAIS
                    elif estado == "ARC" and palavra[0].isdigit():
                        if len(partes) < 3:
                            print(f" Linha ARC inválida: {linha}")
                            continue
                        de = int(partes[0])
                        para = int(partes[1])
                        custo = int(partes[2])
                        self.arcos_opcionais.append((de, para, custo, 0, 0))
                        self.adj_arcos[de].append((para, custo))

                except Exception as e:
                    print(f" Erro ao processar linha: '{linha}'\n   → {e}")
                    continue
                            


    
    # analiseGrafo.py (CONTINUAÇÃO - estatísticas)

    def grau_vertices(self):
        graus = [len(self.adj_arestas[v]) + len(self.adj_arcos[v]) for v in range(1, self.num_vertices + 1)]
        return min(graus), max(graus)

    def densidade(self):
        total_elementos = len(self.adj_arestas) + len(self.adj_arcos)
        max_elementos = self.num_vertices * (self.num_vertices - 1)
        return total_elementos / max_elementos if max_elementos != 0 else 0

    def componentes_conectados(self):
        visitado = [False] * (self.num_vertices + 1)
        componentes = 0

        def dfs(v):
            stack = [v]
            while stack:
                u = stack.pop()
                if not visitado[u]:
                    visitado[u] = True
                    for viz, _ in self.adj_arestas[u]:
                        if not visitado[viz]:
                            stack.append(viz)

        for v in range(1, self.num_vertices + 1):
            if not visitado[v]:
                dfs(v)
                componentes += 1
        return componentes

    def dijkstra(self, origem):
        dist = [math.inf] * (self.num_vertices + 1)
        prev = [-1] * (self.num_vertices + 1)
        dist[origem] = 0
        fila = [(0, origem)]

        while fila:
            custo, atual = heapq.heappop(fila)
            if custo > dist[atual]:
                continue
            for viz, peso in self.adj_arestas[atual] + self.adj_arcos[atual]:
                if dist[viz] > dist[atual] + peso:
                    dist[viz] = dist[atual] + peso
                    prev[viz] = atual
                    heapq.heappush(fila, (dist[viz], viz))
        return dist, prev

    def gerar_matrizes_caminhos(self):
        n = self.num_vertices
        self.matriz_custos = np.full((n + 1, n + 1), np.inf)
        self.matriz_predecessores = np.full((n + 1, n + 1), -1)

        for v in range(1, n + 1):
            dist, prev = self.dijkstra(v)
            self.matriz_custos[v] = dist
            self.matriz_predecessores[v] = prev

    def caminho_medio_e_diametro(self):
        total = 0
        count = 0
        diametro = 0

        for i in range(1, self.num_vertices + 1):
            for j in range(1, self.num_vertices + 1):
                if i != j and self.matriz_custos[i][j] < math.inf:
                    total += self.matriz_custos[i][j]
                    count += 1
                    diametro = max(diametro, self.matriz_custos[i][j])

        caminho_medio = total / count if count > 0 else 0
        return caminho_medio, diametro

    def centralidade_intermediacao(self):
        centralidade = [0] * (self.num_vertices + 1)
        for s in range(1, self.num_vertices + 1):
            _, prev = self.dijkstra(s)
            for t in range(1, self.num_vertices + 1):
                if s != t:
                    atual = t
                    while prev[atual] != -1 and prev[atual] != s:
                        centralidade[prev[atual]] += 1
                        atual = prev[atual]
        return centralidade
    
    def algoritmo_guloso(self):
        self.gerar_matrizes_caminhos()
        deposito = self.deposito
        capacidade_veiculo = self.capacidade

        todos_servicos = self.todos_servicos.copy()
        nao_atendidos = set(s[1] for s in todos_servicos)
        rotas = []
        custo_total = 0

        while nao_atendidos:
            carga = 0
            custo_rota = 0
            rota = [f"(D 0,1,1)"]
            atual = deposito

            algum_atendido = False  # FLAG para evitar loop infinito

            while True:
                melhor_servico = None
                melhor_dist = float('inf')

                for s in todos_servicos:
                    tipo, sid, de, para, custo, demanda = s
                    if sid not in nao_atendidos:
                        continue
                    if carga + demanda > capacidade_veiculo:
                        continue

                    dist = self.matriz_custos[atual][de]
                    if dist < melhor_dist:
                        melhor_dist = dist
                        melhor_servico = s

                if not melhor_servico:
                    break

                tipo, sid, de, para, custo, demanda = melhor_servico
                nao_atendidos.remove(sid)
                custo_rota += self.matriz_custos[atual][de] + custo
                carga += demanda

                tripla = self.gerar_tripla_servico(melhor_servico, atual)
                rota.append(tripla)
                atual = para
                algum_atendido = True

            if not algum_atendido:
                print(" Erro: Nenhum serviço pôde ser atendido com a capacidade disponível.")
                print(f"Serviços restantes: {len(nao_atendidos)} — capacidade: {capacidade_veiculo}")
                for s in todos_servicos:
                    tipo, sid, _, _, _, demanda = s
                    if sid in nao_atendidos and demanda > capacidade_veiculo:
                        print(f"⚠️ Serviço impossível de atender (demanda {demanda} > capacidade): SID {sid}")
                        nao_atendidos.remove(sid)
                break

            rota.append(f"(D 0,1,1)")
            rotas.append((carga, custo_rota, rota))
            custo_total += custo_rota

        return custo_total, rotas





    def gerar_tripla_servico(self, servico, origem):
        tipo, sid, de, para, custo, demanda = servico

        # Corrige a direção com base no movimento real (origem atual)
        if origem == para:
            de, para = para, de

        return f"(S {sid},{de},{para})"

    
    def escrever_arquivo_saida(self, nome_saida, rotas, solucao_ref, num_rotas_ref, clocks_ref, clocks_melhor_ref):
        with open(nome_saida, "w") as f:
            f.write(f"{int(solucao_ref)}\n")
            f.write(f"{int(num_rotas_ref)}\n")
            f.write(f"{int(clocks_ref)}\n")
            f.write(f"{int(clocks_melhor_ref)}\n")
            for i, (carga, custo, caminho) in enumerate(rotas, 1):
                total_visitas = len(caminho)
                f.write(f" 0 1 {i} {carga} {int(custo)} {total_visitas} {' '.join(caminho)}\n")



