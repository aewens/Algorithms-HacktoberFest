from collections import deque, namedtuple

infinity = float("inf")
Edge = namedtuple("Edge", ["start", "end", "cost"])

class Graph:
    def __init__(self, edges):
        invalid_edges = list()
        self.edges = list()

        for edge in edges:
            if len(edge) in [1, 2]:
                invalid_edges.append(edge)

            self.edges.append(self.make_edge(*edge))

        assert not invalid_edges, f"Invalid edges: {invalid_edges}"

    def make_edge(self, start, end, cost=1):
        return Edge(start, end, cost)

    def make_node_pairs(self, node1, node2, both_ends=True):
        if both_ends:
            return [[node1, node2], [node2, node1]]

        return [[node1, node2]]

    def get_vertices(self):
        edge_points = ([edge.start, edge.end] for edge in self.edges)
        # NOTE - Will turn ([a, b], [c, d]) into [a, b, c, d]
        collapse_edges = sum(edge_points, [])

        # NOTE - Will remove duplicates
        return set(collapse_edges)

    def get_neighbors(self):
        neighbors = {vertex: set() for vertex in self.get_vertices()}

        for edge in self.edges:
            neighbors[edge.start].add((edge.end, edge.cost))

        return neighbors

    def add_edge(self, node1, node2, cost=1, both_ends=True):
        node_pairs = self.make_node_pairs(node1, node2, both_ends)

        for edge in self.edges:
            if node_pairs in [edge.start, edge.end]:
                raise Exception(f"Edge {node1} {node2} already exist")

        self.edges.append(self.make_edge(node1, node2, cost))
        if both_ends:
            self.edges.append(self.make_edge(node2, node1, cost))

    def remove_edge(self, node1, node2, both_ends=True):
        # NOTE - Makes a copy of the list
        edges = self.edges[:]
        node_pairs = self.make_node_pairs(node1, node2, both_ends)

        for edge in edges:
            if node_pairs in [edge.start, edge.end]:
                self.edges.remove(edge)

    def compute(self, source, destination):
        self_vertices = self.get_vertices()
        assert source in self_vertices, f"Source node does not exist"

        prev_vertices = {vertex: None for vertex in self_vertices}
        distances = {vertex: infinity for vertex in self_vertices}
        distances[source] = 0
        neighbors = self.get_neighbors()
        vertices = self_vertices.copy()

        while vertices:
            current_vertex = min(vertices, key=lambda v: distances[v])

            if distances[current_vertex] == infinity:
                break

            for neighbor, cost in neighbors[current_vertex]:
                other_route = distances[current_vertex] + cost

                if other_route < distances[neighbor]:
                    distances[neighbor] = other_route
                    prev_vertices[neighbor] = current_vertex

            vertices.remove(current_vertex)

        # NOTE - Think of deque as a list you can push/pop from the start or end
        path, current_vertex = deque(), destination

        while prev_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = prev_vertices[current_vertex]

        if path:
            path.appendleft(current_vertex)

        return list(path)

if __name__ == "__main__":
    graph = Graph([
        ("a", "b", 5), ("a", "c", 9), ("a", "f", 4),
        ("b", "c", 7), ("b", "d", 5), ("c", "d", 8),
        ("c", "f", 2), ("d", "e", 6), ("e", "f", 9)
    ])

    print(graph.compute("b", "f")) # ["b", "c", "f"]
