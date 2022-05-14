class Node:
    def __init__(self, parent):

        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)

        self.children = []

        self.value = 0
        self.board = None

    def is_root(self):
        return self.parent is None

    def add_child(self, child):
        self.children.append(child)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

    def get_children(self):
        return self.children

    def render(self, level):
        print(f"{' ' * level}{self}", flush=True)
        for child in self.children:
            child.render(level + 1)

    def init_own_children(self, stop_depth, curr_depth):
        if stop_depth < curr_depth:
            return
        for i in range(1, 8):
            tmp = Node(self)
            tmp.init_own_children(stop_depth, curr_depth + 1)

    def write_result(self, result, UID):
        if len(UID) > 1:
            return self.children[UID.pop(0)].write_result(UID)
        else:
            self.children[UID[0]].set_value(result)
            return True
