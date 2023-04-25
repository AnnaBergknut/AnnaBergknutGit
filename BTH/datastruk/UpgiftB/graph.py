
class Graph():
    """Docstring"""
    def __init__(self):
        pass

    def add_vertex(self, vertex: str) -> None:
        pass

    def add_edge(self, source: str, target: str, weight: int) -> None:
        pass

    def clear(self) -> None:
        pass

    def get_edge(self, source: str, target: str) -> int:
        pass

    def mst(self) -> None:
        pass

    def save_mst_to_file(self, filepath: str) -> None:
        pass
        
    def read_graph_from_file(self, filepath: str) -> None:
        for line in open(filepath, 'r', encoding='UTF-8'):
            data = line.rstrip().split()
            self.add_edge(str(data[0]),str(data[1]),int(data[2]))
