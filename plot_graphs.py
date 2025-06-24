import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
from graph_competencias import GraphCompetences
from typing import List, Union, overload, Optional, Dict

@overload
def bar_plot(
    columns: List[str],
    names: List[str],
    values: List[List[float]],
    show: bool = False
):
    """
    Does a grouped bar plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        The names for each element in the array of values.
    `values`:
        An array of values 1-D for each element in `names`.

    Keyword Args
    ------------
    `show`:
        If settled, will show the generated image before return it.
    """
    ...

def bar_plot(
    columns: List[str],
    names: Union[str, List[str]],
    values: Union[List[List[float]], List[float]],
    show: bool = False,
    constant_lines: Optional[Union[Dict[str, float], List[Dict[str, float]]]] = None,
    colors: Optional[Union[str, List[str]]] = None

):
    """
    Does a grouped bar plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        Can be a list of names or a single name. If empty, will not plot any legend
    `values`:
        An array of 1-D float lists or a single 1-D array of floats

    Keyword Args
    ------------
    `show`:
        If settled, will show the generated image before return it.
    """

    data: List[any] = []
    isGrouped: bool = (type(names) is list) and (type(values[0]) is list)

    # Processa as cores
    if colors is not None:
        if isinstance(colors, str) or len(colors) == 1:
            color_seq = [colors] * len(values) if isGrouped else [colors]
        else:
            color_seq = colors
    else:
        color_seq = None

    if not isGrouped:

        bar = go.Bar(
            name=names,
            x=columns,
            y=values,
            text=values,
            textposition='auto',
            marker_color=color_seq if color_seq else None
        )

        data.append(bar)  # type: ignore

    else:
        # appending bar plots

        for idx, (k, v) in enumerate(zip(names, values)):
            bar = go.Bar(
                name=k,
                x=columns,
                y=v,
                text=v,
                textposition='auto',
                marker_color=color_seq[idx] if color_seq else None
            )
            data.append(bar)  # type: ignore
    fig = go.Figure(data)  # type: ignore

    # Add constant lines if provided
    if constant_lines:
        if isinstance(constant_lines, dict):
            constant_lines = [constant_lines]
        
        for line in constant_lines:
            fig.add_hline(
                y=line['y'],
                line_color=line.get('color', 'red'),
                line_dash=line.get('dash', 'dash'),
                annotation_text=line.get('name', ''),
                annotation_position="top right",
                opacity=line.get('opacity', 0.5)
            )
    # Change the bar mode
    if isGrouped:
        fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
        fig.update_layout(barmode='group', uniformtext_minsize=1,
                          uniformtext_mode='show', width=1000)
    if show:
        fig.show()

    return fig  # type: ignore

def spider_plot(
    columns: List[str],
    names: Union[str, List[str]],
    values: Union[List[List[float]], List[float]],
    show: bool = False):
    """
    Does spider plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        Can be a list of names or a single name. If empty, will not plot any legend
    `values`:
        An array of 1-D float lists or a single 1-D array of floats

    Keyword Args
    ------------
    `show`:
        If settled will not show the figure at end

    Returns
    -------
    FigureWidget
        A figure plotly object (only access by ipykernel)

    Todo
    ----
    Missing treat exceptions
    """

    # creating a new figure
    fig = go.Figure()  # type: ignore

    isGrouped: bool = (type(names) is list) and (type(values[0]) is list)
    if not isGrouped:
        fig.add_trace(go.Scatterpolar(  # type: ignore
            r=values,
            theta=columns,
            fill='toself',
            name=names))
    else:
        # adding traces

        for k, v in zip(names, values):
            fig.add_trace(go.Scatterpolar(  # type: ignore
                r=v,
                theta=columns,
                fill='toself',
                name=k))

        fig.update_traces(texttemplate='%{text:.2f}')
        fig.update_layout(barmode='group', uniformtext_minsize=1,
                          uniformtext_mode='show', width=1000)

    # show this object
    if show:
        fig.show()

    # and return it
    return fig

def plot_graph(graph_competences:GraphCompetences):
    """
    Plot the directed graph using matplotlib.

    Args:
    ----
    graph_competences: GraphCompetences
        An instance of GraphCompetences containing the graph data.
    Argumentos:
    ----------
    graph_competences: GraphCompetences
        Uma instância de GraphCompetences contendo os dados do grafo.
    """

    G = graph_competences.G 
    pos = graph_competences.pos
    pos_node_attr = {}
    for node, (x, y) in pos.items():
        pos_node_attr[node] = (x, y - 0.06)

    node_labels = {}
    for n, d in G.nodes(data=True):
        if 'G_dp' in d:
            node_labels[n] = ('Gdp', d['G_dp'])

    edge_labels = {(u, v): f"Cdp, {d['weight']}" for u, v, d in G.edges(data=True)}

    plt.figure(figsize=(10, 10))  # Adjust the size as needed

    # Draw the graph
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_shape="o",
        node_size=4000,
        font_size=8,
        font_color="black",
        node_color="skyblue",
        edge_color="gray",
    )

    nx.draw_networkx_labels(G, pos=pos_node_attr, labels=node_labels, font_color="black", font_size=7)
    nx.draw_networkx_edge_labels(
        G,
        pos=pos,
        edge_labels=edge_labels,
        label_pos=0.28,
        bbox=dict(boxstyle="round,pad=0.5", edgecolor="none", alpha=0.5),
        horizontalalignment='center',
        verticalalignment='center',
        rotate=False,
        font_color="black",
        font_size=7,
    )
    plt.show()