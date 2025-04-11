class ColaMisiones:
    def __init__(self):
        self.items = []

    def enqueue(self, mision):
        self.items.append(mision)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def first(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def listar(self):
        return self.items