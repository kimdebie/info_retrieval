import pandas as pd
import csv
import random
from collections import defaultdict

filename = "../data/YandexRelPredChallenge.txt"

def load_data(data):
    '''This function loads data into an appropriate form for further analysis.
    Input: Yandex Click Log file
    Output: a pandas dataframe with rows of format [QueryID, [ResultIDs], [Clicked]]'''

    completed_queries = []
    rank = 3

    with open(data) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:

            if row[2] == 'Q':
                try:
                    completed_queries.append(query)
                except:
                    pass
                query = row
                query.append([])
                query.append([])

                for i in range(5, rank+5):
                    query[15].append(query[i])
                    query[16].append(False)

            else:
                for i in range(0, rank):
                    if row[3] == query[15][i]:
                        query[16][i] = True

    headers = ['SessionID', 'TimePassed', 'TypeOfAction', 'QueryID', 'RegionID', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'ResultIDs', 'Clicked']
    qd_pairs = pd.DataFrame(completed_queries, columns=headers)
    qd_pairs = qd_pairs[['QueryID', 'ResultIDs', 'Clicked']]

    return qd_pairs

def learn_model_parameters(qd_pairs):

    '''This method takes as input the Yandex click log. It trains the alpha and
     gamma parameters for the PBM model on the basis of this file. It saves the
    alphas and gammas (so they only have to be trained once) to a csv and
    returns them.'''

    iterations = 50

    ## EM algorithm for finding optimal alpha and gamma ##

    # Set parameters to initial values
    max_rank = 3
    alphas = defaultdict(lambda: 0.5)
    gammas = [0.5] * max_rank

    for ctr in range(0, iterations):
        print("Round " + str(ctr))

        print("Update alphas")

        # update one alpha for each QD pair
        new_alphas = defaultdict(lambda:1)
        qd_count = defaultdict(lambda:2)

        for i, session in qd_pairs.iterrows():

            if i%10000 == 0:
                print(str(i) + " sessions visited")

            for rank in range(max_rank):
                query = session["QueryID"]
                result = session["ResultIDs"][rank]
                click_u = float(session["Clicked"][rank])

                old_alpha = max(alphas[(query, result)], 0.000001)
                old_gamma = max(gammas[rank], 0.000001)

                qd_count[(query, result)] += 1

                # add new weights to dictionary
                new_alphas[(query, result)] += click_u + (1-click_u) * \
                ((1-old_gamma)*old_alpha / (1-old_gamma*old_alpha))

        for key, value in qd_count.items():
            new_alphas[key] /= value

        alphas = new_alphas


        print("Update gammas")

        new_gammas = [0] * max_rank

        # update one gamma per rank
        for i, session in qd_pairs.iterrows():

            if i%10000 == 0:
                print(str(i) + " sessions visited")

            for rank in range(max_rank):
                query = session["QueryID"]
                result = session["ResultIDs"][rank]
                click_u = float(session["Clicked"][rank])
                old_gamma = gammas[rank]
                old_alpha = alphas[(query, result)]

                new_gammas[rank] += click_u + (1-click_u) * \
                    (old_gamma*(1-old_alpha)) / (1-old_gamma*old_alpha)

        for rank, value in enumerate(gammas):
            gammas[rank] = new_gammas[rank] / qd_pairs.shape[0]

        print(gammas)

    alphas_df = pd.DataFrame.from_dict(alphas, orient='index')
    alphas_df.to_csv('../data/trained_alphas.csv')

    gammas_df = pd.DataFrame({'gammas': gammas})
    gammas_df.to_csv('../data/trained_gammas.csv')

    return alphas, gammas

#alphas, gammas = learn_model_parameters(data)

def get_gammas_from_file():
    '''Use this method to load gammas when parameters are already trained.'''

    try:
        gammas = pd.read_csv('../data/trained_gammas.csv')
        gammas = gammas['gammas'].tolist()

        return gammas

    except:
        print("File not found!")

def predict_click_probability(ranked_list, gammas):

    '''This method takes as input a ranked list (Interleaved.list) and a list
    of gamma parameters that determine the examination probability per rank.
    The method calculates its own alpha parameters. It returns the click
    probabilities of the ranked list (also as a list).'''

    # set epsilon to small value (prob that a not-relevant document is clicked)
    epsilon = 1e-6

    click_probabilities = []

    for rank, item in enumerate(ranked_list):

        relevance = item[0]

        # check relevance label to determine alphas
        if relevance == 1:
            alpha = 1-epsilon
        else:
            alpha = epsilon

        # determine gamma
        gamma = gammas[rank]

        click_prob = alpha * gamma
        click_probabilities.append(click_prob)

    return click_probabilities



def click_documents(ranked_list, click_probabilities):

    '''This method takes as input a ranked list of documents (Interleaved.list)
    and the click probabilities for each rank. It returns a list of the same
    length with Booleans indicating whether a document was clicked or not.'''

    clicked = []

    for rank, item in enumerate(ranked_list):

        rand = random.uniform(0, 1)

        if rand < click_probabilities[rank]:
            click = True
        else:
            click = False

        clicked.append(click)

    return clicked

def random_click_model(qd_pairs):

    '''This method takes the dataset with all sessions and returns the click
    probabilities trained using the random click model. Probabilities are returned
    in a length of maximum rank for convenience.'''
    max_rank = 3
    clicks = 0
    docs = 0

    for i, session in qd_pairs.iterrows():
        for rank in range(max_rank):
            docs += 1
            if session["Clicked"][rank]:
                clicks += 1

    click_prob = clicks / docs

    click_probs = [click_prob] * max_rank

    return click_probs

def get_model_parameters():
    """
    Tries to take gammas from a file, if the file doesn't exist train
    parameters to get the gammas.
    """
    gammas = get_gammas_from_file()
    if not gammas == None:
        return gammas
    else:
        _, gammas = learn_model_parameters(data)
        return gammas
