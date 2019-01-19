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
        raise notImplementedError

if __name__ == "__main__":
    E_ranking = [{"id":1, "relevance":1}, {"id":2, "relevance":1}, {"id":3, "relevance":0}]
    P_ranking = [{"id":3, "relevance":0}, {"id":2, "relevance":1}, {"id":6, "relevance":1}]

    E = Ranking(E_ranking)
    P = Ranking(P_ranking)
    pair = Pair(E, P)
    i_list = Interleaved(pair)
    for i in range(1):
        i_list.team_draft()
    print("Interleaving:", i_list.list)
