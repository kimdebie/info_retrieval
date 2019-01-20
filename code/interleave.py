"class Ranking:\n",
"    def __init__(self, ranker, ranking_list):\n",
"        self.id = 0\n",
"        self.ranker = E\n",
"        self.ranking = [{id: 1, relevance: 0}, {id: 2, relevance: 0}, {id: 3, relevance: 1}]\n",
"        self.ERR = calculate_ERR(self.ranking)\n",
"        \n",
"        #ids tussen 1 en 6. Voor E altijd 1 2 3.\n",

"class Pair:\n",
"    def __init__(self, ranking_E, ranking_P):\n",
"        self.rankings = [ranking_E, ranking_P]\n",
"        self.delta_ERR = ranking_E.ERR - ranking_P.ERR\n",
"        \n",
"    def test_possibility():\n",
"        # BRAM HET IS NOG NIET AF!!!!! TODO\n",
"        raise notImplementedError()    \n",
"        \n",
import random
import copy

class Ranking:
    def __init__(self, ranking_list):
        self.id = 0
        self.ranking = ranking_list
        self.ERR = self.calculate_ERR()

        #ids tussen 1 en 6. Voor E altijd 1 2 3.

    def calculate_ERR(self):
        return 1

class Pair:
    def __init__(self, ranking_E, ranking_P):
        self.rankings = [ranking_E, ranking_P]
        self.delta_ERR = ranking_E.ERR - ranking_P.ERR

    def test_possibility():
        # BRAM HET IS NOG NIET AF!!!!! TODO
        raise notImplementedError()

class Interleaved:
    def __init__(self, pair):
        """
        blablabla
        """
        self.pair = pair
        self.list = None

    def team_draft(self):
        """
        Takes the rankings in pair and merges them using team draft
        interleaving. The interleaved list contains tuples of form
        (relevance, ranker).
        """
        interleaved_list = []
        available_E = set([i["id"] for i in self.pair.rankings[0].ranking])
        available_P = set([i["id"] for i in self.pair.rankings[1].ranking])
        available = available_E.union(available_P)
        team = [0,0]

        while len(available_E.intersection(available)) > 0 \
                and len(available_P.intersection(available)) > 0:

            # Flip a coin to determine which ranker is first
            ranker = int(team[0] > team[1] or (team[0] == team[1]
                         and random.choice([0,1]) == 1))

            for document in self.pair.rankings[ranker].ranking:
                if document["id"] in available:
                    interleaved_list.append((document["relevance"], ranker))
                    available.remove(document["id"])
                    team[ranker] += 1
                    break


        self.list = interleaved_list

    def probabilistic(self):
        # Get lists l1 and l2 and interleaved list l
        l1 = copy.copy(self.pair.rankings[0].ranking)
        l2 = copy.copy(self.pair.rankings[1].ranking)
        lists = [l1, l2]
        interleaved_list = []

        # As long as some thing is still true: TODO: This may be wrong
        while len(l1) > 0 and len(l2) > 0:

            # Randomly select one of the lists
            ranker = random.choice([0,1])
            random_l = lists[ranker]

            # Sample d from lx using a softmax
            document_rank = self.sample_softmax(len(random_l))
            document = random_l[document_rank]

            # Put d in l and remove from l1 and l2
            interleaved_list.append((document["relevance"], ranker))
            for l in lists:
                try:
                    l.remove(document)
                except ValueError:
                    pass

        self.list = interleaved_list

    def sample_softmax(self, length):
        """
        Returns an integer from 0 to length according to a softmax
        function.
        """
        normalization = sum([1/i**3 for i in range(1, length + 1)])

        sample = random.random()
        total = 0

        for i in range(1, length + 1):
            total += (1/i**3)/normalization
            if sample < total:
                return i - 1

        # You should never get here error
        raise notImplementedError()

if __name__ == "__main__":
    E_ranking = [{"id":1, "relevance":1}, {"id":2, "relevance":1}, {"id":3, "relevance":0}]
    P_ranking = [{"id":2, "relevance":1}, {"id":3, "relevance":0}, {"id":6, "relevance":1}]

    E = Ranking(E_ranking)
    P = Ranking(P_ranking)
    pair = Pair(E, P)
    i_list = Interleaved(pair)

    average = 0
    N = 10**5
    for i in range(N):
        i_list.probabilistic()
        average += sum([i[1] for i in i_list.list])/len(i_list.list)
    print("Average:", average/N)
