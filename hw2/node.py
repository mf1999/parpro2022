ILLEGAL_MOVE = 100


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
        print(f"{' ' * level}{self.value}", flush=True)
        for child in self.children:
            child.render(level + 1)

    def init_own_children(self, stop_depth, curr_depth):
        if stop_depth < curr_depth:
            return
        for i in range(1, 8):
            tmp = Node(self)
            tmp.init_own_children(stop_depth, curr_depth + 1)

    def write_results(self, results, UID):
        if len(UID) > 1:
            child_idx = UID.pop(0)
            self.children[child_idx].set_value(results.pop(0))
            return self.children[child_idx].write_results(results, UID)
        else:
            self.children[UID[0]].set_value(results[0])
            return True

    def run_heuristic(self, depth):
        if self.value == 1:
            pass
        elif self.value == -1:
            pass
        elif self.value == ILLEGAL_MOVE:
            pass
        else:# self.value == 0:
            if len(self.children) == 0:
                pass
            else:
                ctr_legal = 0
                for child in self.children:
                    child.run_heuristic(depth + 1)
                    if child.get_value() != ILLEGAL_MOVE:
                        ctr_legal += 1
                        if depth % 2 == 1:
                            #CPU MOVE
                            if child.get_value() == -1:
                                self.value = -1
                                return
                            else:
                                self.value += child.get_value()
                        else:
                            if child.get_value() == 1:
                                self.value = 1
                                return
                            else:
                                self.value += child.get_value()
                if self.value != 0:
                    self.value = self.value / ctr_legal

