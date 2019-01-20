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

    def test_possibility():
        raise notImplementedError()

def calculate_ERR(ranking):

    rl1, rl2, max = 0, 0, 0

    # find maximum of relevance labels
    for idx, docu in enumerate(ranking):
        rl = docu['relevance']

        # store relevance label of first and second document
        if idx == 0:
            rl1 = rl
        elif idx == 1:
            rl2 = rl

        # update maximum
        if rl > max:
            max = rl

    # calculate probability of stopping at first and second document
    prob1 = (2**rl1-1)/(2**max)
    prob2 = (2**rl2-1)/(2**max)

    # calculate ERR as sum of products
    ERR = 0
    for i in range(2,4):

        if i == 2:
            prod2 = (1 - prob1) * prob1 * (1 / i)
            ERR += prod2

        elif i == 3:
            prod3 = (1 - prob1) * prob1 * (1 - prob2) * prob2 * (1 / i)
            ERR += prod3

    return ERR

def main():

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

            # Adjust relevance labels & id numbers
            for j, document_P in enumerate(rank_P.ranking):
                document_P['relevance'] = rl_perm[j]
                document_P['id'] = id_perm[j]

            # calculate ERR
            rank_P.set_ERR()

            # store ranking list for P
            rankings_P.append(rank_P)
            id += 1

    # combine pairs
    pairs = []

if __name__ == '__main__':
    main()
