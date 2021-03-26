class GraphEvent:
    def __init__(self, graph):
        self.callbacks = []
        self.graph = graph

    def __call__(self, *args, **kwargs):
        return [cb(*args, **kwargs) for cb in self.callbacks]

    def add(self, cb):
        if not callable(cb):
            raise TypeError("Must be callable object")
        self.callbacks.append(cb)
