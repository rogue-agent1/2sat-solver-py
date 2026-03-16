#!/usr/bin/env python3
"""2-SAT solver — implication graph + Kosaraju/Tarjan SCC."""

class TwoSAT:
    def __init__(self, n):
        self.n = n; self.graph = [[] for _ in range(2*n)]
        self.rgraph = [[] for _ in range(2*n)]
    def _var(self, x): return 2*x if x >= 0 else 2*(-x-1)+1
    def _neg(self, v): return v ^ 1
    def add_clause(self, a, b):
        """a OR b, where a/b are signed: +x means x, -x means NOT (x-1)."""
        va, vb = self._var(a), self._var(b)
        # NOT a => b, NOT b => a
        self.graph[self._neg(va)].append(vb)
        self.graph[self._neg(vb)].append(va)
        self.rgraph[vb].append(self._neg(va))
        self.rgraph[va].append(self._neg(vb))
    def solve(self):
        n2 = 2 * self.n; order = []; visited = [False]*n2
        def dfs1(u):
            visited[u] = True
            for v in self.graph[u]:
                if not visited[v]: dfs1(v)
            order.append(u)
        for i in range(n2):
            if not visited[i]: dfs1(i)
        comp = [-1]*n2; c = 0
        def dfs2(u, c):
            comp[u] = c
            for v in self.rgraph[u]:
                if comp[v] == -1: dfs2(v, c)
        for u in reversed(order):
            if comp[u] == -1: dfs2(u, c); c += 1
        for i in range(self.n):
            if comp[2*i] == comp[2*i+1]: return None
        return [comp[2*i] > comp[2*i+1] for i in range(self.n)]

def main():
    sat = TwoSAT(3)
    sat.add_clause(0, 1)    # x0 OR x1
    sat.add_clause(-1, 2)   # NOT x0 OR x2
    sat.add_clause(-2, -3)  # NOT x1 OR NOT x2
    result = sat.solve()
    print(f"Solution: {result}")

if __name__ == "__main__": main()
