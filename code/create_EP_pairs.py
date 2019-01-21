class Ranking:

    def __init__(self, id, ranker):
        self.id = id
        self.ERR = 0
        self.ranker = ranker
        self.ranking = [{'id': 1, 'relevance': 0}, {'id': 2, 'relevance': 0}, {'id': 3, 'relevance': 0}]

    def set_ERR(self):
        self.ERR = calculate_ERR(self.ranking)

class Pair:
    def __init__(self, ranking_E, ranking_P):
        self.rankings = [ranking_E, ranking_P]
        self.delta_ERR = ranking_E.ERR - ranking_P.ERR

def calculate_ERR(ranking):

    rl1, rl2, max = 0, 0, 1

    # find relevance labels of first and second document
    for idx, docu in enumerate(ranking):
        rl = docu['relevance']

        if idx == 0:
            rl1 = rl
        elif idx == 1:
            rl2 = rl

    # calculate probability of stopping at first and second document
    prob1 = (2**rl1-1)/(2**max)
    prob2 = (2**rl2-1)/(2**max)
    probs = [prob1, prob2]

    # calculate ERR as sum of products
    ERR = 0
    for r in range(len(probs)):
        temp = 1
        for i in range(r):
            temp *= 1-probs[i]
        ERR += temp*probs[r]/(r+1)

    return ERR

def main():

    """
    This function creates two ranked lists of documents for algorithm P and E.
    Subsequently, it forms E-P pairs of possible rankings.
    """

    ############### CREATE RANKED LIST FOR E ###############

    rankings_E = []
    rankings_P = []

    # define all possible combinations of relevance labels
    rl_permutations = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]

    # assign id to the rankings
    id = 0

    # iterate over permutations of relevance labels
    for rl_perm in rl_permutations:

        # create ranking object and adjust its relevance labels
        rank_E = Ranking(id, 'E')
        for i, document_E in enumerate(rank_E.ranking):
             document_E['relevance'] = rl_perm[i]

        # calculate ERR
        rank_E.set_ERR()

        # store ranking list for E
        rankings_E.append(rank_E)
        id += 1

    ############### CREATE RANKED LIST FOR P ###############

    # define all possible id's for P
    id_permutations = [[1, 5, 6], [2, 5, 6], [3, 5, 6], [4, 5, 6], \
                       [4, 1, 6], [4, 2, 6], [4, 3, 6], \
                       [4, 5, 1], [4, 5, 2], [4, 5, 3], \
                       [1, 2, 6], [1, 5, 2], [4, 1, 2], \
                       [1, 3, 6], [1, 5, 3], [4, 1, 3], \
                       [2, 3, 6], [2, 5, 3], [4, 2, 3], \
                       [2, 1, 6], [2, 5, 1], [4, 2, 1], \
                       [3, 1, 6], [3, 5, 1], [4, 3, 1], \
                       [3, 2, 6], [3, 5, 2], [4, 3, 2], \
                       [1, 2, 3], [1, 3, 2], [3, 1, 2], [3, 2, 1], [2, 1, 3], [2, 3, 1]]

    # iterate over possible id's for P
    for id_perm in id_permutations:

        # iterate over permutations of relevance labels
        for rl_perm in rl_permutations:

            # create ranking object for P
            rank_P = Ranking(id, 'P')

            # adjust relevance labels & id numbers
            for j, document_P in enumerate(rank_P.ranking):
                document_P['relevance'] = rl_perm[j]
                document_P['id'] = id_perm[j]

            # calculate ERR
            rank_P.set_ERR()

            # store ranking list for P
            rankings_P.append(rank_P)
            id += 1

    ############### FORM E-P PAIRS ###############

    pairs = []

    for rank_E in rankings_E:

        # store ids and relevance labels of E
        ids_E = [1, 2, 3]
        rl_E = [d.get('relevance') for d in rank_E.ranking]

        for rank_P in rankings_P:

            # keep track of errors (duplicates with non-matching rl's)
            error = False

            # store ids and relevance labels of P
            ids_P = [d.get('id') for d in rank_P.ranking]
            rl_P = [d.get('relevance') for d in rank_P.ranking]

            # iterate over ids of P
            for idx, id in enumerate(ids_P):

                # check for duplicates with non-matching relevance labels
                if (id in ids_E) & (rl_P[idx] != rl_E[idx]):
                    error = True
                    break

            # create pair and add to list, if no error occurs
            if not error:
                pair = Pair(rank_E, rank_P)
                pairs.append(pair)

    return pairs

def create_groups(pairs):
    """
    This function seperates pairs into groups based on delta_ERR intervals.
    It returns a list of sublists; each sublists contains an object of class Pair
    """

    group1 = [p for p in pairs if (p.delta_ERR>=0.05 and p.delta_ERR<0.1)]
    group2 = [p for p in pairs if (p.delta_ERR>=0.1 and p.delta_ERR<0.2)]
    group3 = [p for p in pairs if (p.delta_ERR>=0.2 and p.delta_ERR<0.3)]
    group4 = [p for p in pairs if (p.delta_ERR>=0.3 and p.delta_ERR<0.4)]
    group5 = [p for p in pairs if (p.delta_ERR>=0.4 and p.delta_ERR<0.5)]
    group6 = [p for p in pairs if (p.delta_ERR>=0.5 and p.delta_ERR<0.6)]
    group7 = [p for p in pairs if (p.delta_ERR>=0.6 and p.delta_ERR<0.7)]
    group8 = [p for p in pairs if (p.delta_ERR>=0.7 and p.delta_ERR<0.8)]
    group9 = [p for p in pairs if (p.delta_ERR>=0.8 and p.delta_ERR<0.9)]
    group10 = [p for p in pairs if (p.delta_ERR>=0.9 and p.delta_ERR<=0.95)]

    data = [group1, group2, group3, group4, group5, group6, group7, \
            group8, group9, group10]
    return data

if __name__ == '__main__':
    pairs = main()
    data = create_groups(pairs)
