from collections import defaultdict
import copy
import pandas as pd

class Graph:

    def __init__(self, num_vertices, idx2pos, pos2pers):
        
        # graph information maintained through out program process
        self.tot_vertices = num_vertices
        # key of index number with values,
        # list of preferred position index
        self.savedGraph = defaultdict(list)



        # number of vertices
        # modified every deleted cycle
        self.num_vertices = num_vertices

        # idx2pos dictionary 
        # calculations done with idx number
        # dictionary used to output as wanted position number
        self.idx2pos = idx2pos

        # pos2pers dictionary 
        # calculations done with position number
        # dictionary used to output as wanted position number
        self.pos2pers = pos2pers

        # initiated through myFunction init_graph at main
        # init_graph(graph, data, pos2idx)
        # dictionary of key as idx of vertices with 
        # value list of preferred idx
        self.graph = defaultdict(list)

        # dictionary of score saved as value
        # to each idx number vertices as key
        self.staff_scores = defaultdict(int)



        # holds the information of all cycle and its score and vertex size
        # recorded during findMaxCycle()
        self.record = defaultdict(list)

        # holds the information of selected cycles
        self.max_cycles = []
        self.left_vertices = []


        self.score_records = defaultdict(list)
        self.max_scores = []
    

    # called from my function to save score
    # to each vertices according to idx number
    def saveScore(self, u, score):
        self.staff_scores[u] = score
    

    # called from my function to add hiring manager score
    # to each staff on certain position according to idx number
    def addScore(self, u):
        self.staff_scores[u] += 1

    # called from my function to add edges
    # according to the preferred idx number 
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


    
    
    
    
    
    
    # finds mobility according to maximum cycle size
    def find_max_cycles(self):
        while self.graph:

            # records cycles and its scores
            self.recordMaxCycles()
            
            # remove cycles according to cycle length
            self.removeMaxCycle()
    
    # finds mobility according to cycle score
    def find_max_score_cycles(self):

        # records cycles and its scores
        # until there is no vertex left in graph
        while self.graph:

            # records cycles and its scores
            self.recordMaxCycles()

            # remove cycles according to cycle score
            self.removeMaxScore()
    






    def recordMaxCycles(self):

        # cleans saved cycle records, and scores
        # then begin finding information about cycle
        self.record = defaultdict(list)
        self.score_records = defaultdict(list)

        # loops over each vertices in graph
        # as the start of building cycles 
        for start in self.graph:
            score_stack = []

            # append the score of the first vertex,
            # no need to add the vertex itself to stack
            # because it is indicated as the start of the cycle
            # just the score
            # score_stack.append(self.num_vertices**self.staff_scores[start])
            score_stack.append(self.staff_scores[start]**2)

            stack = []
            self.DFS(start, start, self.record[start], stack, self.score_records[start], score_stack)
    
    def DFS(self, start, u, route_stacks, stack, score_rec, score_stack):
        if u in self.graph:

            # if it is not the end of cycle
            if start != u:
                # save the current vertex
                # as it is a vertex part of searching cycle
                stack.append(u)

                # save the current vertex score
                # as if is a vertex part of seraching cycle
                # score_stack.append(self.num_vertices**self.staff_scores[u])
                score_stack.append(self.staff_scores[u]**2)

            # loop through the edges of this vertex
            # as this vertex is part of searching cycle
            for v in self.graph[u]:

                # if the next cycle is not searched (colored)
                if v not in stack:

                    # if it is the end of the searching cycle
                    if v == start:

                        # appends both cycle route and scores to standard data structure
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

            # loop through all the cycles recorded
            for j in range(len(self.record[i])):

                # save the length of the cycle
                cyc_len = len(self.record[i][j])

                # save the vertex, cycle, length information
                # of the largest cycle
                if cyc_len > max[l]:
                    max[v] = i
                    max[c] = j
                    max[l] = cyc_len
        
        if max[v] != -1:

            # add position for printing out results
            self.record[max[v]][max[c]].append(max[v])

            # record the finalized maxed cycle to data structure
            self.max_cycles.append(self.record[max[v]][max[c]])
            
            self.printCurrentMaxCycle(max)

            cnt = 0
            # delete the vertex related to the cycle
            for cyc_vertex in self.record[max[v]][max[c]]:
                del self.graph[cyc_vertex]
                cnt += 1

            # edit the vertex number size
            # according to the number of vertices deleted in the total graph 
            self.num_vertices -= cnt
        else:
            print('left alone positions: ', end='')
            
            self.left_vertices = list(self.graph.keys())
            
            for pos in self.left_vertices:
                print(self.idx2pos[pos], end=', ')
                del self.graph[pos]
    


    def removeMaxScore(self):
        v = 'vertex'
        c = 'cycle'
        l = 'score'

        max = {v: -1, c: -1, l: -1}

        for i in self.score_records:

            # loop through all the scores recorded for a single cycle
            for j in range(len(self.score_records[i])):

                # save the score of the cycle                
                cyc_score = sum(self.score_records[i][j])

                # save the vertex, cycle, score information
                # of the maximum score cycle
                if cyc_score > max[l]:
                    max[v] = i
                    max[c] = j
                    max[l] = cyc_score
        
        if max[v] != -1:
            # add position for printing out results
            self.record[max[v]][max[c]].append(max[v])

            # record the finalized max score cycle to the data structure
            self.max_cycles.append(self.record[max[v]][max[c]])
            
            self.printCurrentMaxCycle(max)

            cnt = 0
            # delete the certex related to the cycle
            for cyc_vertex in self.record[max[v]][max[c]]:
                del self.graph[cyc_vertex]
                cnt += 1

            # edit the vertex number size
            # according to the number of vertices deleted in the total graph 
            self.num_vertices -= cnt
        else:
            print('left alone positions: ', end='')
            
            self.left_vertices = list(self.graph.keys())
            
            for pos in self.left_vertices:
                print(self.idx2pos[pos], end=', ')
                del self.graph[pos]







    # save result of mobilty to an excel file 
    # according to the max cycles selected and saved
    def saveExcel(self):
        mobility = []

        total_mob_cnt = 0
        # iter through found mobility cycles
        for cycle in self.max_cycles:

            # iter through each position in cycle
            for v in range(1, len(cycle)+1, 1):

                # when current position is not the last position in the cycle
                if v < len(cycle):
                    from_pos = self.idx2pos[cycle[v-1]]
                    to_pos = self.idx2pos[cycle[v]]
                
                # when current position is the last position in the cycle
                # match it with the first positoin
                else:
                    from_pos = self.idx2pos[cycle[v-1]]
                    to_pos = self.idx2pos[cycle[0]]



                total_mob_cnt += 1

                mobility.append([
                    total_mob_cnt,
                    from_pos,
                    self.pos2pers[from_pos]['first_name'],
                    self.pos2pers[from_pos]['last_name'],
                    self.pos2pers[from_pos]['title'],
                    self.pos2pers[from_pos]['level'],
                    self.pos2pers[from_pos]['duty_station'],
                    self.pos2pers[from_pos]['hardship'],
                    to_pos,
                    self.pos2pers[to_pos]['first_name'],
                    self.pos2pers[to_pos]['last_name'],
                    self.pos2pers[to_pos]['title'],
                    self.pos2pers[to_pos]['level'],
                    self.pos2pers[to_pos]['duty_station'],
                    self.pos2pers[to_pos]['hardship'],
                ])
        
        for v in range(len(self.left_vertices)):
            from_pos = self.idx2pos[self.left_vertices[v]]

            mobility.append([
                    total_mob_cnt,
                    from_pos,
                    self.pos2pers[from_pos]['first_name'],
                    self.pos2pers[from_pos]['last_name'],
                    self.pos2pers[from_pos]['title'],
                    self.pos2pers[from_pos]['level'],
                    self.pos2pers[from_pos]['duty_station'],
                    self.pos2pers[from_pos]['hardship'],
                ])
        
        df = pd.DataFrame(mobility, columns=[
                'num',
                'from',
                'first name',
                'last name',
                'position title',
                'level',
                'duty station',
                'hardship classification',
                'to',
                'first name',
                'last name',
                'position title',
                'level',
                'duty station',
                'hardship classification',
            ])

        df.to_excel('result.xlsx')