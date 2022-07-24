import math

def mk_pos2idx(data):
    pos2idx = {}

    idx = 0

    for i, row in data.iterrows():
        pos_num = row[0]

        if pos_num not in pos2idx:
            pos2idx[pos_num] = idx
            idx += 1
    
    return pos2idx

def print_pos2idx(pos2idx):
    key_list = list(pos2idx.keys())

    for key in key_list:
        print(key, end=': ')
        print(pos2idx[key])

def init_graph(graph, data, pos2idx):

    for i, row in data.iterrows():
        pos_idx = pos2idx[row[0]]
        pref_pos_list = list(row[5:8])
        
        for pref_pos in pref_pos_list:
            if not math.isnan(pref_pos):
                pref_int = int(pref_pos)
                pref_idx = pos2idx[pref_int]

                graph.addEdge(pos_idx, pref_idx)

def print_graph(graph):
    key_list = list(graph.keys())

    for key in key_list:
        print(key, end=': ')

        for pref_pos in graph[key]:
            print(pref_pos, end='-->')
        
        print()

def to_idx2pos(pos2idx):
    idx2pos = {}
    for key in pos2idx:
        idx2pos[pos2idx[key]] = key
    
    return idx2pos

