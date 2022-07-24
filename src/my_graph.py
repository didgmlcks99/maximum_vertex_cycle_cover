from collections import defaultdict
import copy

class Graph:

    def __init__(self, vertices, idx2pos):
        self.V = vertices
        self.graph = defaultdict(list)
        self.idx2pos = idx2pos
        self.record = defaultdict(list)
    
    def addEdge(self, u, v):
        self.graph[u].append(v)
    
    def printGraph(self):
        for i in self.graph:
            print(i, end=': ')
            for pref in self.graph[i]:
                print(pref, end=', ')
            print()

        print('*************************')

        for i in self.graph:
            print(self.idx2pos[i], end=': ')
            for pref in self.graph[i]:
                print(self.idx2pos[pref], end=', ')
            print()
    
    def printRecord(self):
        
        for i in self.record:
            print(i, end=': ')
            for route in self.record[i]:
                print(route, end=', ')
            print()
    
    def printMaxCycle(self, max):
        v = 'vertex'
        c = 'cycle'
        l = 'length'
        
        print(max)
        print(self.idx2pos[max[v]], end=' --> ')
        for nxt_pos in self.record[max[v]][max[c]]:
            print(self.idx2pos[nxt_pos], end=' --> ')
        print()

        # print(max)
        # print(max[v], end=' --> ')
        # for nxt_pos in self.record[max[v]][max[c]]:
        #     print(nxt_pos, end=' --> ')
        # print()

    
    def find_max_cycles(self):

        while self.graph:
            self.recordMaxCycles()
            self.removeMaxCycle()
            print()
    
    def recordMaxCycles(self):
        self.record = defaultdict(list)
        
        for start in self.graph:
            stack = []
            self.DFS(start, start, self.record[start], stack)
    
    def DFS(self, start, u, route_stacks, stack):

        if u in self.graph:
            if start != u:
                stack.append(u)

            for v in self.graph[u]:
                if v not in stack:
                    if v == start:
                        route_stacks.append(copy.deepcopy(stack))
                    else:
                        self.DFS(start, v, route_stacks, stack)
            
            if stack:
                stack.pop()
    
    def removeMaxCycle(self):
        v = 'vertex'
        c = 'cycle'
        l = 'length'

        max = {v: -1, c: -1, l: -1}

        for i in self.record:
            for j in range(len(self.record[i])):
                cyc_len = len(self.record[i][j])

                if cyc_len > max[l]:
                    max[v] = i
                    max[c] = j
                    max[l] = cyc_len
        
        if max[v] != -1:
            self.printMaxCycle(max)

            for cyc_vertex in self.record[max[v]][max[c]]:
                del self.graph[cyc_vertex]
            
            del self.graph[max[v]]
        else:
            print('left alone positions: ', end='')
            
            left_pos = list(self.graph.keys())
            
            for pos in left_pos:
                print(self.idx2pos[pos], end=', ')
                del self.graph[pos]

            # for pos in left_pos:
            #     print(pos, end=', ')
            #     del self.graph[pos]