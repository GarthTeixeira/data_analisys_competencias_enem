import networkx as nx
from typing import List, Dict

class GraphCompetences:

    def __init__(self, raw_graph, num_anos = 3, razao_minima = 0.5):
        """
        Initialize the GraphCompetences class with raw graph data.
        Inicializa a classe GraphCompetences com dados brutos do grafo.

        Args:
        ----
        raw_graph: List[Dict]
            The raw graph data containing nodes and edges.
        num_anos: int
            The number of years to consider in the graph (default is 3).

        Argumentos:
        ----------
        raw_graph: List[Dict]
            Os dados brutos do grafo contendo nós e arestas.

        num_anos: int
            O número de anos a considerar no grafo (padrão é 3).
        """
        self.ano_final = num_anos
        self.G, self.pos = self.create_graph(raw_graph) # Referente ao passo 9
        print(f"Graph created with {len(self.G.nodes)} nodes and {len(self.G.edges)} edges.")
        self.propagar_valores() # Referente ao passo 10
        self.output_competencia = self.G.nodes['Aprovado'].get('acumulador', 0)
        self.aluno_maximo = GraphCompetences.calcular_aluno_maximo(num_anos,self.G)
        self.aluno_minimo = self.aluno_maximo * razao_minima
        
    def create_graph(self, raw_graph:List[Dict]) -> tuple[nx.DiGraph, Dict]:
        """
        Create a directed graph from the raw graph data.
        Criar o grafo direcionado a partir dos dados do grafo bruto.

        Args:
        ----
        raw_graph: List[Dict]
            The raw graph data containing nodes and edges.

        Argumentos:
        ----------

        raw_graph: List[Dict]
            Os dados brutos do grafo contendo nós e arestas.

        Returns:
        -------
        G:nx.DiGraph
            A directed graph object.
        pos: Dict
            A dictionary containing the positions of the nodes in the graph.

        Retorno:
        -------
        G:nx.DiGraph
            Um objeto de grafo direcionado.
        pos: Dict
            Um dicionário contendo as posições dos nós no grafo.
        """
        # Initialize position count for each year
        pos_count = {i: 0 for i in range(1, self.ano_final + 1)}
        edges = []
        nodes = []
        pos = {}

        def make_node_name(txt, serie_ano):
            name = txt.replace(" ", "\n")
            return name + ' - ' + str(serie_ano) if name != 'Aprovado' else name

        # Create nodes and edges
        for item in raw_graph:
            u = item['u']
            node_name = make_node_name(u['nome'], u['serie_ano'])
            node_attr = {"G_dp": round(item['G_dp'],3), "id": str(u['_id'])}
            nodes.append((node_name, node_attr))
            pos[node_name] = (u['serie_ano'], pos_count[u['serie_ano']])
            pos_count[u['serie_ano']] += 1
            for v in item['v']:
                edges.append((node_name, make_node_name(v['nome'], v['serie_ano']), {"weight": round(item["C_dp"], 3)}))

        nodes.append("Aprovado")
        pos['Aprovado'] = (4, (max(list(pos_count.values())) / 2) - 0.5)

        # Create the graph
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        return G, pos

    def propagar_valores(self,gdp_attr='G_dp',acumulador_attr='acumulador'):
        """
        Propaga valores em um grafo direcionado com base no G_dp e peso das arestas.

        Parâmetros:
            G: networkx.DiGraph
            gdp_attr: nome do atributo G_dp em cada nó
            peso_attr: nome do atributo weight em cada aresta
            acumulador_attr: nome do atributo acumulador a ser criado nos nós

        Resultado:
            O grafo G terá um novo atributo em cada nó chamado 'acumulador' (ou nome especificado).
        """

        # Inicializar acumuladores
        acumulador = {node: 0 for node in self.G.nodes}

        # Obter os G_dp de cada nó
        gdp_por_no = {node: self.G.nodes[node].get(gdp_attr, 0) for node in self.G.nodes}

        # Executar propagação em ordem topológica
        try:
            ordem = list(nx.topological_sort(self.G))
        except nx.NetworkXUnfeasible:
            raise ValueError("O grafo contém ciclos; propagação só funciona em grafos acíclicos (DAGs).")

        for node in ordem:
            for succ in self.G.successors(node):
                peso = self.G.edges[node, succ].get('weight', 1)
                contribuicao = (gdp_por_no[node] + acumulador[node]) * peso
                acumulador[succ] += contribuicao

        # Armazenar no grafo
        for node in self.G.nodes:
            self.G.nodes[node][acumulador_attr] = acumulador[node]

    @staticmethod
    def somatorio_arestas_entrada(G:nx.DiGraph, node:str) -> float:
        return sum(data.get('weight', 0) for _, _, data in G.in_edges(node, data=True))


    @staticmethod
    def somador_por_ano_completo(ano_final:int, somatorio_dpc:Dict,x=0)->float:
        if ano_final > 1:
            return x + somatorio_dpc[ano_final] * GraphCompetences.somador_por_ano_completo(ano_final - 1, somatorio_dpc, 1)
        else:
            return 1 + somatorio_dpc[ano_final]


    @staticmethod
    def calcular_aluno_maximo(ano_final:int, G:nx.DiGraph)-> float:
        """
        simula o máximo que um aluno da turma pode alcançar
        em termos de notas, considerando as competências e áreas avaliadas.
        Args:
        ----
        G: networkx.DiGraph
            O grafo direcionado que representa as competências e áreas avaliadas.
        Returns:
        ----
        aluno_maximo: float
            O valor máximo que o aluno pode alcançar.
        """

        ##Somatorio de cdp por ano do nó
        
        somatorio_cdp = {i: 0 for i in range(1, ano_final + 1)}
        ano_final =  ano_final
        for key in somatorio_cdp.keys():
            if(ano_final == key):
                somatorio_cdp[key] = GraphCompetences.somatorio_arestas_entrada(G, "Aprovado")
            else:
                node = list(filter (lambda x: str(key+1) in x, G.nodes))[0]
                somatorio_cdp[key] += GraphCompetences.somatorio_arestas_entrada(G, node)

        #Para conferir o somatório
        #print(somatorio_cdp)

        return GraphCompetences.somador_por_ano_completo(3,somatorio_cdp)