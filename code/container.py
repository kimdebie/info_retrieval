############################ Interleaved cell

class Interleaved:
    def __init__(self, pair):
        """
        A class containing a pair of rankings, has methods to interleave
        these rankings into a list as well as counters to keep track of how
        often pair.rankings[0] (or E) wins.
        input:
            pair: A Pair object as defined earlier in the notebook
        """
        self.pair = pair
        self.list = None
        self.wins_team_draft = 0
        self.wins_probabilistic = 0

    def team_draft(self):
        """
        Modifies self.list in place.
        Takes the rankings in self.pair and merges them using team draft
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


        self.list = interleaved_list[:3]

    def probabilistic(self):
        """
        Modifies self.list in place.
        Takes the rankings in self.pair and merges them using probabilistic
        interleaving. The interleaved list contains tuples of form
        (relevance, ranker).
        """
        l1 = copy.copy(self.pair.rankings[0].ranking)
        l2 = copy.copy(self.pair.rankings[1].ranking)
        lists = [l1, l2]
        interleaved_list = []

        # As long as some thing is still true:
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

        self.list = interleaved_list[:3]

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

####################################### Complete project cell

def online_experiment(interleaving, gammas, k):
    for i in range(k):
        interleaving.team_draft()
        click_documents(interleaving, predict_click_probability(interleaving, gammas))

        interleaving.probabilistic()
        click_documents(interleaving, predict_click_probability(interleaving, gammas))

def simulate_experiment(pairs, gammas, k):

    interleavings = []
    for pair in pairs:
        interleaving = Interleaved(pair)

        online_experiment(interleaving, gammas):

        interleavings.append(interleaving)

    return interleavings
