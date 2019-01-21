import pandas as pd
import csv
import random
from collections import defaultdict

data = "../data/YandexRelPredChallenge.txt"

def learn_model_parameters(data):

    '''This method takes as input the Yandex click log. It first cleans the file
    and then trains the alpha and gamma parameters for the PBM model on the basis
    of this file. It saves the alphas and gammas (so they only have to be trained
    once) to a csv and returns them.'''

    # Cleaning data

    completed_queries = []

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
                for i in range(5, 11):
                    query[15].append(query[i])
                    query[i] = False

            else:
                for i in range(0, 6):
                    if row[3] == query[15][i]:
                        query[i+5] = True

    headers = ['SessionID', 'TimePassed', 'TypeOfAction', 'QueryID', 'RegionID', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'ResultIDs']
    data = pd.DataFrame(completed_queries, columns=headers)
    #print(data.head())

    query_doc_pairs = [] #[queryID-docID, rank, clicked]
    for index, query in data.iterrows():
        for i, doc in enumerate(query['ResultIDs']):
            row = [str(query['QueryID']) + '-' + str(doc), i, query[i]]
            query_doc_pairs.append(row)

    headers2 = ["QueryDocPair", "Rank", "Clicked"]
    qd_pairs = pd.DataFrame(query_doc_pairs, columns=headers2)


    ## EM algorithm for finding optimal alpha and gamma ##

    # Set parameters to initial values

    # alpha (attractiveness) is defined per unique query-document pair
    alphas = {}
    for index in qd_pairs["QueryDocPair"].unique():
        alphas[index] = 1
    print("Total alphas to be trained: " + str(len(alphas)))

    # gamma (examination) is defined per rank
    gammas = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    # As we are primarily interested in gammas (we will discard alphas)
    # convergence is determined on the basis of gammas.
    delta_gammas = 1
    rounds = 0

    while delta_gammas > 0.05:
        print("Round " + str(rounds))
        rounds+= 1

        print("Update alphas")

        # update one alpha for each QD pair
        new_alphas = defaultdict(lambda:1)
        qd_count = defaultdict(lambda:2)
        
        for i, session in qd_pairs.iterrows():
            if i%1000 == 0:
                print(str(i) + " parameters trained in this round")

            # getting the relevant parameters for the formula
            click_u = session["Clicked"]
            old_gamma = gammas[session["Rank"]]
            old_alpha = alphas[session["QueryDocPair"]]

            # The Formula
            new_alphas[session["QueryDocPair"]] += click_u + (1-click_u) * \
             ((1-old_gamma)*old_alpha / 1-old_gamma*old_alpha)

            qd_count[session["QueryDocPair"]] += 1

        for key, value in qd_count.items():
            new_alphas[key] /= value

        alphas = new_alphas



        for i, index in enumerate(qd_pairs["QueryDocPair"].unique()):

            if i%1000 == 0:
                print(str(i) + " parameters trained in this round")

            # take alpha and all sessions for this particular Q-D pair
            sess_qd = qd_pairs[qd_pairs["QueryDocPair"] == index]
            old_alpha = alphas[index]

            # following the update formula for each session
            sum_of_clicks_alpha = 1
            for i, session in sess_qd.iterrows():

                # getting the relevant parameters for the formula
                click_u = session["Clicked"]
                old_gamma = gammas[session["Rank"]]

                # The Formula
                sum_of_clicks_alpha += click_u + (1-click_u) * \
                 ((1-old_gamma)*old_alpha / 1-old_gamma*old_alpha)

            # final update to this alpha
            alphas[index] = 1/(sess_qd.shape[0]+2) * sum_of_clicks_alpha


        print("Update gammas")

        # track change in deltas to determine convergence
        delta_gammas = 0

        # update one alpha per rank
        for rank, gamma in enumerate(gammas):

            # take all sessions and the gamma for this particular rank
            sess_rank = qd_pairs[qd_pairs["Rank"] == rank]
            old_gamma = gammas[rank]

            sum_of_clicks_gamma = 0
            for i, session in sess_rank.iterrows():

                click_u = session["Clicked"]
                old_alpha = alphas[session["QueryDocPair"]]

                sum_of_clicks_gamma += click_u + (1-click_u) * \
                (old_gamma*(1-old_alpha) / 1-old_gamma*old_alpha)

            gammas[rank] = 1/len(sess_rank) * sum_of_clicks_gamma
            delta_gammas += abs(gammas[rank] - old_gamma)

        print(gammas)
        print("Change in gammas: " + str(delta_gammas))

    alphas_df = pd.DataFrame.from_dict(alphas, orient='index')
    alphas_df.to_csv('../data/trained_alphas.csv')

    gammas_df = pd.DataFrame({'gammas': gammas})
    gammas_df.to_csv('../data/trained_gammas.csv')

    return alphas, gammas

alphas, gammas = learn_model_parameters(data)

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
