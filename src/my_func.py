import math

# makes a diction of position id to index number
def mk_pos2idx(data):
    pos2idx = {}

    idx = 0

    for i, row in data.iterrows():
        pos_num = row[0]

        if pos_num not in pos2idx:
            pos2idx[pos_num] = idx
            idx += 1
    
    return pos2idx

# create new dictionary for idx2pos
# for further convenience
def to_idx2pos(pos2idx):
    idx2pos = {}
    for key in pos2idx:
        idx2pos[pos2idx[key]] = key
    
    return idx2pos

# inits graph
def init_graph(graph, data, pos2idx):

    # index numbers to access each data 
    # in data
    position = 0
    start_pref = 5
    end_pref = 8
    total_score = 13


    # loop through each applications in data (from excel)
    for i, row in data.iterrows():
        
        # save the idx number assigned to that specific position number
        # according to given pos2idx dictionary 
        idx_num = pos2idx[row[position]]

        # list of preferred positions saved
        pref_pos_list = list(row[start_pref:end_pref])
        
        # total score 
        tot_score = row[total_score]

        # save the total score 
        # assigned to the vertex 
        # by idx number
        # idx_num : total score
        graph.saveScore(idx_num, tot_score)
        

        # loop through each preferred position
        for pref_pos in pref_pos_list:

            # if it is not an error input (it is a number)
            if not math.isnan(pref_pos):

                pref_int = int(pref_pos)

                # save the idx number of the preferred position number
                # by pos2idx dictionary
                pref_idx = pos2idx[pref_int]

                # add an edge to the vertex of current idx_num to the pref_idx
                graph.addEdge(idx_num, pref_idx)

# tool function to print pos2idx dictionary
def print_pos2idx(pos2idx):
    key_list = list(pos2idx.keys())

    for key in key_list:
        print(key, end=': ')
        print(pos2idx[key])

# tool function to print graph and visualize
def print_graph(graph):
    key_list = list(graph.keys())

    for key in key_list:
        print(key, end=': ')

        for pref_pos in graph[key]:
            print(pref_pos, end='-->')
        
        print()