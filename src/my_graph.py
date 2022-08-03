from collections import defaultdict
import copy

class Graph:

    def __init__(self, vertices, idx2pos, n):
        self.V = vertices
        self.savedGraph = defaultdict(list)
        self.graph = defaultdict(list)
        self.idx2pos = idx2pos
        self.record = defaultdict(list)
        self.max_cycles = []
        self.left_vertices = []

        self.staff_scores = defaultdict(int)
        self.n = n

        self.score_records = defaultdict(list)
        self.max_scores = []
    
    def saveScore(self, u, score):
        self.staff_scores[u] = score
    
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.savedGraph[u].append(v)
    
    def printGraph(self):
        for i in self.savedGraph:
            print(i, end=': ')
            for pref in self.savedGraph[i]:
                print(pref, end=', ')
            print()

        print('*************************')

        for i in self.savedGraph:
            print(self.idx2pos[i], end=': ')
            for pref in self.savedGraph[i]:
                print(self.idx2pos[pref], end=', ')
            print()
    
    def printRecord(self):
        for i in self.record:
            print(i, end=': ')
            for route in self.record[i]:
                print(route, end=', ')
            print()
    
    def printCurrentMaxCycle(self, max):
        v = 'vertex'
        c = 'cycle'
        l = 'length'
        
        print(max)
        print(self.idx2pos[max[v]], end=' > ')
        for nxt_pos in range(len(self.record[max[v]][max[c]])):
            print(self.idx2pos[self.record[max[v]][max[c]][nxt_pos]], end='')
            if nxt_pos != len(self.record[max[v]][max[c]])-1: print('', end=' > ')
            else: print()

        # print(max)
        # print(max[v], end=' --> ')
        # for nxt_pos in self.record[max[v]][max[c]]:
        #     print(nxt_pos, end=' --> ')
        # print()
    
    def printResult(self):
        for cycle in self.max_cycles:
            for v in range(len(cycle)):
                print(self.idx2pos[cycle[v]], end='')
                if v != len(cycle)-1: print('', end=' > ')
                else: print()
        
        print('left out positions: ', end='')
        for v in range(len(self.left_vertices)):
            print(self.idx2pos[self.left_vertices[v]], end='')
            if v != len(self.left_vertices)-1: print('', end=', ')
            else: print()

    def find_max_cycles(self):
        while self.graph:
            self.recordMaxCycles()
            self.removeMaxCycle()
            print()
    
    def find_max_score_cycles(self):
        while self.graph:
            self.recordMaxCycles()
            self.removeMaxScore()
            print()
    
    def recordMaxCycles(self):
        self.record = defaultdict(list)
        self.score_records = defaultdict(list)
        
        for start in self.graph:
            score_stack = []
            score_stack.append(self.n**self.staff_scores[start])

            stack = []
            self.DFS(start, start, self.record[start], stack, self.score_records[start], score_stack)
    
    def DFS(self, start, u, route_stacks, stack, score_rec, score_stack):
        if u in self.graph:
            if start != u:
                stack.append(u)
                score_stack.append(self.n**self.staff_scores[u])

            for v in self.graph[u]:
                if v not in stack:
                    if v == start:
                        route_stacks.append(copy.deepcopy(stack))
                        score_rec.append(copy.deepcopy(score_stack))
                    else:
                        self.DFS(start, v, route_stacks, stack, score_rec, score_stack)
            
            # remove going back track (DFS)
            if stack:
                stack.pop()
                score_stack.pop()
    
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
            self.record[max[v]][max[c]].append(max[v])
            self.max_cycles.append(self.record[max[v]][max[c]])
            
            self.printCurrentMaxCycle(max)

            for cyc_vertex in self.record[max[v]][max[c]]:
                del self.graph[cyc_vertex]
        else:
            print('left alone positions: ', end='')
            
            self.left_vertices = list(self.graph.keys())
            
            for pos in self.left_vertices:
                print(self.idx2pos[pos], end=', ')
                del self.graph[pos]

            # for pos in self.left_vertices:
            #     print(pos, end=', ')
            #     del self.graph[pos]
    
    def removeMaxScore(self):
        v = 'vertex'
        c = 'cycle'
        l = 'score'

        max = {v: -1, c: -1, l: -1}

        for i in self.score_records:
            for j in range(len(self.score_records[i])):
                cyc_score = sum(self.score_records[i][j])

                if cyc_score > max[l]:
                    max[v] = i
                    max[c] = j
                    max[l] = cyc_score
        
        if max[v] != -1:
            self.record[max[v]][max[c]].append(max[v])
            self.max_cycles.append(self.record[max[v]][max[c]])
            
            self.printCurrentMaxCycle(max)

            for cyc_vertex in self.record[max[v]][max[c]]:
                del self.graph[cyc_vertex]
        else:
            print('left alone positions: ', end='')
            
            self.left_vertices = list(self.graph.keys())
            
            for pos in self.left_vertices:
                print(self.idx2pos[pos], end=', ')
                del self.graph[pos]

            # for pos in self.left_vertices:
            #     print(pos, end=', ')
            #     del self.graph[pos]