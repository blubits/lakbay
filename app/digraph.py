"""
Helper classes for the digraph data structure.

:Author:     Maded Batara III
:Version:    v5.0 (2016-03-29)
"""

class Digraph:
    """
    A weighted, directed graph.

    A graph is a set of vertices, linked together by edges. More formally, it
    is the ordered pair G = (V, E) where V is a set of vertices and E is a
    set containing two-element subsets of V that describe connections
    between vertices.

    This class implements a weighted, directed graph. A directed graph
    is asymmetrical: the existence of an edge (i, j) does not mean there
    is an edge (j, i), and so edges have direction. A weighted graph has
    weights or distances associated with a particular edge.

    The class is partially immutable - the number of vertices cannot be edited,
    but the edges between existing vertices can be added to or removed from.

    Vertices are represented as numbers from 0 to v-1, where v is the number
    of vertices. A mapping of numbers to objects can be used to have graphs
    with objects as vertices, such as a map or a social network.
    """

    def __init__(self, num_vertices):
        """
        Constructs a new graph.

        Args:
            num_vertices (int): Number of vertices in the graph.
        """
        self._num_vertices = num_vertices
        self._num_edges = 0
        self._graph = [set() for i in range(num_vertices)]

    def __str__(self):
        """
        Returns a string representation of the graph.
        """
        strs = []
        for idx, adj in enumerate(self._graph):
            if len(adj) != 0:
                strs.append("{0}: \n\t".format(idx))
                for edge in adj:
                    strs.append("{0}, ".format(edge))
                strs.append("\n")
        return ''.join(strs)

    @property
    def num_vertices(self):
        """
        Number of vertices in the graph.
        """
        return self._num_vertices

    @property
    def num_edges(self):
        """
        Number of edges in the graph.
        """
        return self._num_edges

    def incoming(self, vertex):
        """
        Gets all edges that go to (i.e. incoming) a certain vertex.
        """
        return set(edge for vert in self._graph for edge in vert
                   if edge.vertex_to == vertex)

    def outgoing(self, vertex):
        """
        Gets all edges that come from (i.e. outgoing) a certain vertex.
        """
        return self._graph[vertex]

    def add_edge(self, edge):
        """
        Adds an edge to the graph.

        Args:
            edge (DirectedEdge): Edge to be added to the graph.
        """
        if not (0 <= edge.vertex_from < self._num_vertices and
                0 <= edge.vertex_to < self._num_vertices):
            raise ValueError("Vertex not in graph")
        self._graph[edge.vertex_from].add(edge)
        self._num_edges += 1

    def get_edge(self, frm, to):
        """
        Gets the list of edges that go from one node to another node.

        Args:
            frm (int): Source vertex.
            to (int): Destination vertex.
        """
        if not (0 <= frm < self._num_vertices and
                0 <= to < self._num_vertices):
            raise ValueError("Vertex not in graph")
        return [edge for edge in self.outgoing(frm) if edge.vertex_to == to]

    def has_edge(self, frm, to):
        """
        Checks if an edge exists in the graph.

        Args:
            frm (int): Source vertex.
            to (int): Destination vertex.
        """
        if not (0 <= frm < self._num_vertices and
                0 <= to < self._num_vertices):
            raise ValueError("Vertex not in graph")
        for edge in self.outgoing(frm):
            if edge.vertex_to == to:
                return True
        else:
            return False

class DirectedEdge:
    """
    An edge in the transport network digraph.
    """

    def __init__(self, vertex_from, vertex_to, weight):
        """
        Constructs a transport network edge.

        Args:
            vertex_from (int): Origin of edge (where it came from).
            vertex_to (int): Destination of edge (where is it going to).
            weight (float): Weight of edge.
        """
        self._vertex_from = vertex_from
        self._vertex_to = vertex_to
        self._weight = weight

    def __str__(self):
        """
        Returns a string representation of the edge.
        """
        return "{0}->{1} ({2})".format(
            self._vertex_from, self._vertex_to, self._weight
        )

    def __repr__(self):
        """
        Returns repr(self).
        """
        return "<class DirectedEdge: {0}>".format(str(self))

    def __key(self):
        """
        Returns a 3-tuple representing the edge.
        """
        return (self.vertex_from, self.vertex_to, self._weight)

    def __eq__(self, other):
        """
        Checks if two edges are equal.
        """
        return self.__key() == other.__key()

    def __hash__(self):
        """
        Generates a hash code for the edge.
        """
        return hash(self.__key())

    @property
    def vertex_from(self):
        """
        Node ID of stop where the edge is coming from.
        """
        return self._vertex_from

    @property
    def vertex_to(self):
        """
        Node ID of stop where the edge is going to.
        """
        return self._vertex_to

    @property
    def weight(self):
        """
        Weight of edge.
        """
        return self._weight

    def other(self, vertex):
        """
        Gets the vertex opposite to a node along an edge.
        """
        if vertex == self._vertex_from:
            return self._vertex_to
        if vertex == self._vertex_to:
            return self._vertex_from
        raise ValueError("Vertex is not incident to edge")
