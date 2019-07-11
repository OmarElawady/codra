class SymbolTable:
    def __init__(self):
        self.lookup = {}

    def add(self, name, value):
        if not name in self.lookup:
            self.lookup[name] = []    
        self.lookup[name].append(value)

    def pop(self, name):
        self.lookup[name].pop()

    def get_value(self, name):
        return self.lookup[name][-1]
