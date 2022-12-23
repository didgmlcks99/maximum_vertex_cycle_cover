# makes a dictionary of position number to index number
def mk_pos2idx(data):
    pos2idx = {}

    idx = 0

    # row[0] indicates the position number
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
def init_graph(graph, data, pos2idx, pers2pos):

    # index numbers to access each data 
    # in data
    position = 0
    start_pref = 6
    end_pref = 9
    total_score = 14

    start_HM = 9
    end_HM = 14

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
            if not isNan(pref_pos):

                pref_int = int(pref_pos)

                # save the idx number of the preferred position number
                # by pos2idx dictionary
                pref_idx = pos2idx[pref_int]

                # add an edge to the vertex of current idx_num to the pref_idx
                graph.addEdge(idx_num, pref_idx)

        
        
        # todo: add recommendation to position
        rec_list_id = row[start_HM:end_HM]
        rec_ls = []
        for id in rec_list_id:
            if not isNan(id):
                id_idx = pos2idx[pers2pos[int(id)]]
                rec_ls.append(id_idx)
        graph.addRecomm(idx_num, rec_ls)


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


def isNan(n):
    return n != n


# add score to each staff according to the
# hiring manager recommendation
def addHMRecScore(graph, data, pos2idx):
    start_HM = 9
    end_HM = 14

    for i, row in data.iterrows():

        # get list of recommendation given by a single manager
        list_HM = list(row[start_HM:end_HM])

        for position in list_HM:

            # if this recommendation is trully a position number
            # give addition score to the staff at this position
            # through their idx number
            if not isNan(position):
                score4idx = pos2idx[int(position)]
                graph.addScore(score4idx)


def mk_pos2pers(data):

    # index numbers to access each data 
    # in data
    position = 0
    index_num = 1
    first_name = 2
    last_name = 3
    title = 4
    level = 5
    duty_station = 15
    hardship = 16


    pos2pers = {}
    pers2pos = {}

    # row[0] indicates the position number
    for i, row in data.iterrows():
        pos_num = row[position]
        pers2pos[row[index_num]] = pos_num

        if pos_num not in pos2pers:
            pos2pers[pos_num] = {
                'index_num': row[index_num],
                'first_name': row[first_name],
                'last_name': row[last_name],
                'title': row[title],
                'level': row[level],
                'duty_station': row[duty_station],
                'hardship': row[hardship]
            }
    
    return pos2pers, pers2pos