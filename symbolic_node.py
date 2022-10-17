from utils import *
import numpy as np

class SymbolicNode:
    def __init__(self, degree=0):
        self.f = None
        self.lchild = None
        self.rchild = None
        self.n_child = None
        self.value = None
        self.degree = degree
        self.all_node = []

    def post_order_traverse_recursive(self, x):
        if self.lchild is None and self.rchild is None:
            if self.value is None:
                return x
            else:
                return self.value
        elif self.rchild is None: # sin, cos
            return self.f(self.lchild.post_order_traverse_recursive(x))
        else:
            return self.f(
                self.lchild.post_order_traverse_recursive(x),
                self.rchild.post_order_traverse_recursive(x) )

    def setNode(self, params):
        self.n_child = len(params) - 1

        if len(params) == 1:        # one number
            if params[0] == "x":    #     x
                return
            else:                   #     a number in [-10, 10]
                self.val = params[0]
        elif len(params) == 2:      # sin, cos
            self.f = params[0]
            self.lchild = params[1]
        elif len(params) == 3:      # add sub mul div
            self.f = params[0]
            self.lchild = params[1]
            self.rchild = params[2]

    def random_grow(self, max_degree=10, stop_rate=0.2, x_rate=0.5):
        if self.degree >= max_degree or np.random.rand() < stop_rate:
            if np.random.rand() < x_rate:
                return self
            else:
                self.value = rand_const()
                return self
        else:
            self.f = rand_operator()
            if self.f.nin == 1:
                self.lchild = SymbolicNode(degree=self.degree+1)
                self.lchild.random_grow()
            elif self.f.nin == 2:
                self.lchild = SymbolicNode(degree=self.degree+1)
                self.rchild = SymbolicNode(degree=self.degree+1)
                self.lchild.random_grow()
                self.rchild.random_grow()

    def all_node_level_traverse(self):
        quene = [self]
        self.all_node = []
        while len(quene):
            n = quene.pop(0)
            self.all_node.append(n)
            if n is None:
                pass
            elif (not n.lchild is None) and (n.rchild is None):
                quene.append(n.lchild)
            elif (not n.lchild is None) and (not n.rchild is None):
                quene.append(n.lchild)
                quene.append(n.rchild)
        return self.all_node

    def rand_subtree_index(self):
        i = np.random.randint(len(self.all_node))
        return i

    def mutate_point(self, i=None, x_rate=0.5):
        if i is None:
            i = self.rand_subtree_index()
        # operator node
        if not self.all_node[i].f is None:
            f_new = rand_operator()
            if f_new.nin == self.all_node[i].f.nin:
                print("1-1")
                self.all_node[i].f = f_new
            elif f_new.nin > self.all_node[i].f.nin:
                print("1-2")
                self.all_node[i].f = f_new
                if np.random.rand() < x_rate:
                    new_node = SymbolicNode(self.degree+1)
                else:
                    new_node = SymbolicNode(self.degree+1)
                    new_node.value = rand_const()
                self.all_node[i].rchild = new_node
            else:
                print("1-3")
                self.all_node[i].f = f_new
                self.all_node[i].rchild.__del__()
                self.all_node[i].rchild = None
        # const node
        else:
            if np.random.rand() < x_rate:
                print("2-1")
                self.all_node[i].value = None
            else:
                print("2-2")
                self.all_node[i].value = rand_const()

    def mutate_subtree(self, i=None, stop_rate=0.5, max_degree=10, x_rate=0.5):
        if i is None:
            i = self.rand_subtree_index()
        if not self.all_node[i].lchild is None: del self.all_node[i].lchild
        if not self.all_node[i].rchild is None: del self.all_node[i].rchild
        self.all_node[i].f = None
        self.all_node[i].value = None
        self.all_node[i].random_grow(stop_rate=stop_rate, max_degree=max_degree, x_rate=x_rate)

    def mutate_hoist(self, i=None):
        if i is None:
            while True:
                i = np.random.randint(len(self.all_node))
                if not self.all_node[i].lchild is None:
                    break
        self.all_node[i].all_node_level_traverse()
        j = self.all_node[i].rand_subtree_index()
        self.all_node[i].copy2(self.all_node[i].all_node[j])

    def copy(self):
        new_node = SymbolicNode(degree=self.degree)
        new_node.f = self.f
        new_node.value = self.value
        new_node.n_child = self.n_child
        new_node.value = self.value
        if not self.lchild is None:
            new_node.lchild = self.lchild.copy()
        if not self.rchild is None:
            new_node.rchild = self.rchild.copy()
        return new_node

    def copy2(self, another):
        self.f = another.f
        self.value = another.value
        self.n_child = another.n_child
        self.value = another.value
        if not another.lchild is None:
            self.lchild = another.lchild.copy()
        else:
            self.lchild = None
        if not another.rchild is None:
            self.rchild = another.rchild.copy()
        else:
            self.rchild = None
        return self

    def __str__(self):
        if self.f is None:
            if self.value == None:
                return "x"
            else:
                return str(self.value)
        elif self.f.nin == 1:
            return dict_operators[self.f] + "(" + self.lchild.__str__() + ")"
        else:
            return ("(" + str(self.lchild) + dict_operators[self.f] + str(self.rchild) + ")")

    # def __del__(self):
    #     if not self.lchild is None:
    #         self.lchild.__del__()
    #     elif not self.rchild is None:
    #         self.rchild.__del__()
    #     del self

def test_rand():
    root = SymbolicNode()
    root.random_grow()
    print(root)

def test_traverse():
    root = SymbolicNode()
    l = SymbolicNode(1)
    r = SymbolicNode(1)
    ll = SymbolicNode(1)
    ll = SymbolicNode(1)
    root.setNode([operators[2], l, r])
    l.setNode([operators[0], ll, ll])
    print(root)
    print(root.post_order_traverse_recursive(10))

if __name__ == '__main__':
    test_traverse()
