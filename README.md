# Análise e Solução de Instâncias NEARP
Este projeto implementa a análise e uma solução heurística para instâncias do Problema de Roteamento Rural com Demandas e Capacidades (NEARP). Ele foi desenvolvido em Python e processa instâncias no formato .dat armazenadas na pasta instancia/.

# Estrutura de Pastas
.
├── analiseGrafo.py
├── vizualizarGrafo.ipynb
├── instancia/
│   ├── *.dat                  # Arquivos de instância NEARP
│   ├── listaNomeArquivos.csv # Mapeia IDs para nomes dos arquivos .dat
│   └── reference_values.csv   # Contém valores de referência (ótimos ou melhores conhecidos)


# Funcionalidades
O programa permite:

  Leitura e interpretação completa dos arquivos .dat do NEARP.

  Cálculo de estatísticas de grafos:

    Grau mínimo e máximo dos vértices.

    Densidade da rede.

    Número de componentes conexas.

    Caminho médio e diâmetro.

    Centralidade de intermediação (betweenness).

  Geração de matrizes de caminhos mínimos entre todos os pares (baseado em Dijkstra).

  Implementação de um algoritmo guloso para construir soluções viáveis com múltiplas rotas respeitando a capacidade dos veículos.

  Escrita de arquivo de saída com formato compatível com benchmarks.

# Como Executar
1. Pré-requisitos:

  Python 3.x

  Bibliotecas: numpy

2. Abrir e Executar o Notebook:

  No terminal:
    jupyter notebook vizualizarGrafo.ipynb

  Ou abra no VSCode e execute 


# Dados de Entrada

🔹 Arquivos .dat
Cada arquivo define uma instância com:

Capacidade do veículo

Nó depósito

Número de vértices

Arestas/arcos obrigatórios (com demanda)

Arestas/arcos opcionais (sem demanda)

🔹 listaNomeArquivos.csv
Relaciona IDs com nomes de arquivos .dat.

🔹 reference_values.csv
Contém as melhores soluções conhecidas para comparação.

# Saídas Geradas
Os arquivos gerados pelo notebook seguem o formato esperado por sistemas de benchmark:
9700        # custo total da solução
7           # número de rotas
110         # tempo de execução (em clocks)
80          # tempo da melhor solução encontrada

 0 1 1 3500 1400 4 (D 0,1,1) (S 2,10,15) (S 5,15,20) (D 0,1,1)
 ...
